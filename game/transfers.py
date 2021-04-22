from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING, Type

from dcs.unittype import VehicleType

if TYPE_CHECKING:
    from game import Game
from game.theater import ControlPoint, MissionTarget
from game.theater.supplyroutes import SupplyRoute
from gen.naming import namegen
from gen.flights.flight import Flight, FlightType


@dataclass
class TransferOrder:
    """The base type of all transfer orders.

    A transfer order can transfer multiple units of multiple types.
    """

    #: The location the units are transferring from.
    origin: ControlPoint

    #: The location the units are transferring to.
    destination: ControlPoint

    #: True if the transfer order belongs to the player.
    player: bool

    #: The units being transferred.
    units: Dict[Type[VehicleType], int]

    @property
    def description(self) -> str:
        raise NotImplementedError


@dataclass
class RoadTransferOrder(TransferOrder):
    """A transfer order that moves units by road."""

    #: The current position of the group being transferred. Groups move one control
    #: point a turn through the supply line.
    position: ControlPoint = field(init=False)

    def __post_init__(self) -> None:
        self.position = self.origin

    def path(self) -> List[ControlPoint]:
        supply_route = SupplyRoute.for_control_point(self.position)
        return supply_route.shortest_path_between(self.position, self.destination)

    def next_stop(self) -> ControlPoint:
        return self.path()[0]

    @property
    def description(self) -> str:
        path = self.path()
        if len(path) == 1:
            turns = "1 turn"
        else:
            turns = f"{len(path)} turns"
        return f"Currently at {self.position}. Arrives at destination in {turns}."


@dataclass
class AirliftOrder(TransferOrder):
    """A transfer order that moves units by cargo planes and helicopters."""

    flight: Flight

    @property
    def description(self) -> str:
        return "Airlift"


class Convoy(MissionTarget):
    def __init__(self, origin: ControlPoint, destination: ControlPoint) -> None:
        super().__init__(namegen.next_convoy_name(), origin.position)
        self.origin = origin
        self.destination = destination
        self.transfers: List[RoadTransferOrder] = []

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        if self.is_friendly(for_player):
            return

        yield FlightType.BAI
        yield from super().mission_types(for_player)

    def is_friendly(self, to_player: bool) -> bool:
        return self.origin.captured

    def add_units(self, transfer: RoadTransferOrder) -> None:
        self.transfers.append(transfer)

    def remove_units(self, transfer: RoadTransferOrder) -> None:
        self.transfers.remove(transfer)

    def kill_unit(self, unit_type: Type[VehicleType]) -> None:
        for transfer in self.transfers:
            if unit_type in transfer.units:
                transfer.units[unit_type] -= 1
                return
        raise KeyError

    @property
    def size(self) -> int:
        return sum(sum(t.units.values()) for t in self.transfers)

    @property
    def units(self) -> Dict[Type[VehicleType], int]:
        units: Dict[Type[VehicleType], int] = defaultdict(int)
        for transfer in self.transfers:
            for unit_type, count in transfer.units.items():
                units[unit_type] += count
        return units

    @property
    def player_owned(self) -> bool:
        return self.origin.captured


class ConvoyMap:
    def __init__(self) -> None:
        # Dict of origin -> destination -> convoy.
        self.convoys: Dict[ControlPoint, Dict[ControlPoint, Convoy]] = defaultdict(dict)

    def convoy_exists(self, origin: ControlPoint, destination: ControlPoint) -> bool:
        return destination in self.convoys[origin]

    def find_convoy(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> Optional[Convoy]:
        return self.convoys[origin].get(destination)

    def find_or_create_convoy(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> Convoy:
        convoy = self.find_convoy(origin, destination)
        if convoy is None:
            convoy = Convoy(origin, destination)
            self.convoys[origin][destination] = convoy
        return convoy

    def departing_from(self, origin: ControlPoint) -> Iterator[Convoy]:
        yield from self.convoys[origin].values()

    def travelling_to(self, destination: ControlPoint) -> Iterator[Convoy]:
        for destination_dict in self.convoys.values():
            if destination in destination_dict:
                yield destination_dict[destination]

    def disband_convoy(self, convoy: Convoy) -> None:
        del self.convoys[convoy.origin][convoy.destination]

    def add(self, transfer: RoadTransferOrder) -> None:
        next_stop = transfer.next_stop()
        self.find_or_create_convoy(transfer.position, next_stop).add_units(transfer)

    def remove(self, transfer: RoadTransferOrder) -> None:
        next_stop = transfer.next_stop()
        convoy = self.find_convoy(transfer.position, next_stop)
        if convoy is None:
            logging.error(
                f"Attempting to remove {transfer} from convoy but it is in no convoy."
            )
            return
        convoy.remove_units(transfer)
        if not convoy.transfers:
            self.disband_convoy(convoy)

    def disband_all(self) -> None:
        self.convoys = defaultdict(dict)

    def __iter__(self) -> Iterator[Convoy]:
        for destination_dict in self.convoys.values():
            yield from destination_dict.values()


class PendingTransfers:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.convoys = ConvoyMap()
        self.pending_transfers: List[TransferOrder] = []

    def __iter__(self) -> Iterator[TransferOrder]:
        yield from self.pending_transfers

    @property
    def pending_transfer_count(self) -> int:
        return len(self.pending_transfers)

    def transfer_at_index(self, index: int) -> TransferOrder:
        return self.pending_transfers[index]

    def index_of_transfer(self, transfer: TransferOrder) -> int:
        return self.pending_transfers.index(transfer)

    # TODO: Move airlift arrangements here?
    @singledispatchmethod
    def arrange_transport(self, transfer) -> None:
        pass

    @arrange_transport.register
    def _arrange_transport_road(self, transfer: RoadTransferOrder) -> None:
        self.convoys.add(transfer)

    def new_transfer(self, transfer: TransferOrder) -> None:
        transfer.origin.base.commit_losses(transfer.units)
        self.pending_transfers.append(transfer)
        self.arrange_transport(transfer)

    @singledispatchmethod
    def cancel_transport(self, transfer) -> None:
        pass

    @cancel_transport.register
    def _cancel_transport_air(self, transfer: AirliftOrder) -> None:
        flight = transfer.flight
        flight.package.remove_flight(flight)
        self.game.aircraft_inventory.return_from_flight(flight)

    @cancel_transport.register
    def _cancel_transport_road(self, transfer: RoadTransferOrder) -> None:
        self.convoys.remove(transfer)

    def cancel_transfer(self, transfer: TransferOrder) -> None:
        self.cancel_transport(transfer)
        self.pending_transfers.remove(transfer)
        transfer.origin.base.commision_units(transfer.units)

    def perform_transfers(self) -> None:
        incomplete = []
        for transfer in self.pending_transfers:
            if not self.perform_transfer(transfer):
                incomplete.append(transfer)
        self.pending_transfers = incomplete
        self.rebuild_convoys()

    def rebuild_convoys(self) -> None:
        self.convoys.disband_all()
        for transfer in self.pending_transfers:
            self.arrange_transport(transfer)

    @singledispatchmethod
    def perform_transfer(self, transfer) -> bool:
        raise NotImplementedError

    @perform_transfer.register
    def _perform_transfer_air(self, transfer: AirliftOrder) -> bool:
        if transfer.player != transfer.destination.captured:
            logging.info(
                f"Transfer destination {transfer.destination} was captured. Cancelling "
                "transport."
            )
            transfer.origin.base.commision_units(transfer.units)
            return True

        transfer.destination.base.commision_units(transfer.units)
        return True

    @perform_transfer.register
    def _perform_transfer_road(self, transfer: RoadTransferOrder) -> bool:
        # TODO: Can be improved to use the convoy map.
        # The convoy map already has a lot of the data that we're recomputing here.
        if transfer.player != transfer.destination.captured:
            logging.info(
                f"Transfer destination {transfer.destination.name} was captured."
            )
            self.handle_route_interrupted(transfer)
            return True

        supply_route = SupplyRoute.for_control_point(transfer.destination)
        if transfer.position not in supply_route:
            logging.info(
                f"Route from {transfer.position.name} to {transfer.destination.name} "
                "was cut off."
            )
            self.handle_route_interrupted(transfer)
            return True

        path = transfer.path()
        next_hop = path[0]
        if next_hop == transfer.destination:
            logging.info(
                f"Units transferred from {transfer.origin.name} to "
                f"{transfer.destination.name}"
            )
            transfer.destination.base.commision_units(transfer.units)
            return True

        logging.info(
            f"Units transferring from {transfer.origin.name} to "
            f"{transfer.destination.name} arrived at {next_hop.name}. {len(path) - 1} "
            "turns remaining."
        )
        transfer.position = next_hop
        return False

    @staticmethod
    def handle_route_interrupted(transfer: RoadTransferOrder):
        # Halt the transfer in place if safe.
        if transfer.player == transfer.position.captured:
            logging.info(f"Transferring units are halting at {transfer.position.name}.")
            transfer.position.base.commision_units(transfer.units)
            return

        # If the current position was captured attempt to divert to a neighboring
        # friendly CP.
        for connected in transfer.position.connected_points:
            if connected.captured == transfer.player:
                logging.info(f"Transferring units are re-routing to {connected.name}.")
                connected.base.commision_units(transfer.units)
                return

        # If the units are cutoff they are destroyed.
        logging.info(
            f"Both {transfer.position.name} and {transfer.destination.name} were "
            "captured. Units were surrounded and destroyed during transfer."
        )
