from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING, Type

from dcs.mapping import Point
from dcs.unittype import FlyingType, VehicleType

from game.procurement import AircraftProcurementRequest
from game.utils import meters, nautical_miles
from gen.ato import Package
from gen.flights.ai_flight_planner_db import TRANSPORT_CAPABLE
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.flights.flightplan import FlightPlanBuilder
from game.theater import ControlPoint, MissionTarget
from game.theater.supplyroutes import SupplyRoute
from gen.naming import namegen
from gen.flights.flight import Flight, FlightType

if TYPE_CHECKING:
    from game import Game
    from game.inventory import ControlPointAircraftInventory


class Transport:
    def find_escape_route(self) -> Optional[ControlPoint]:
        raise NotImplementedError

    def description(self) -> str:
        raise NotImplementedError


@dataclass
class TransferOrder:
    """The base type of all transfer orders.

    A transfer order can transfer multiple units of multiple types.
    """

    #: The location the units are transferring from.
    origin: ControlPoint

    #: The location the units are transferring to.
    destination: ControlPoint

    #: The current position of the group being transferred. Groups may make multiple
    #: stops and can switch transport modes before reaching their destination.
    position: ControlPoint = field(init=False)

    #: True if the transfer order belongs to the player.
    player: bool = field(init=False)

    #: The units being transferred.
    units: Dict[Type[VehicleType], int]

    transport: Optional[Transport] = field(default=None)

    def __post_init__(self) -> None:
        self.position = self.origin
        self.player = self.origin.is_friendly(to_player=True)

    @property
    def description(self) -> str:
        if self.transport is None:
            return "No transports available"
        return self.transport.description()

    def kill_all(self) -> None:
        self.units.clear()

    def kill_unit(self, unit_type: Type[VehicleType]) -> None:
        if unit_type in self.units:
            self.units[unit_type] -= 1
            return
        raise KeyError

    @property
    def size(self) -> int:
        return sum(c for c in self.units.values())

    def iter_units(self) -> Iterator[Type[VehicleType]]:
        for unit_type, count in self.units.items():
            for _ in range(count):
                yield unit_type

    @property
    def completed(self) -> bool:
        return self.destination == self.position or not self.units

    def disband_at(self, location: ControlPoint) -> None:
        logging.info(f"Units halting at {location}.")
        location.base.commision_units(self.units)
        self.units.clear()

    def proceed(self) -> None:
        if self.transport is None:
            return

        if not self.destination.is_friendly(self.player):
            logging.info(f"Transfer destination {self.destination} was captured.")
            if self.position.is_friendly(self.player):
                self.disband_at(self.position)
            elif (escape_route := self.transport.find_escape_route()) is not None:
                self.disband_at(escape_route)
            else:
                logging.info(
                    f"No escape route available. Units were surrounded and destroyed "
                    "during transfer."
                )
                self.kill_all()
            return

        self.position = self.destination
        self.transport = None

        if self.completed:
            self.disband_at(self.position)


@dataclass
class Airlift(Transport):
    """A transfer order that moves units by cargo planes and helicopters."""

    transfer: TransferOrder

    flight: Flight

    @property
    def units(self) -> Dict[Type[VehicleType], int]:
        return self.transfer.units

    @property
    def player_owned(self) -> bool:
        return self.transfer.player

    def find_escape_route(self) -> Optional[ControlPoint]:
        # TODO: Move units to closest base.
        return None

    def description(self) -> str:
        return f"Being airlifted by {self.flight}"


class AirliftPlanner:
    #: Maximum range from for any link in the route of takeoff, pickup, dropoff, and RTB
    #: for a helicopter to be considered for airlift. Total route length is not
    #: considered because the helicopter can refuel at each stop. Cargo planes have no
    #: maximum range.
    HELO_MAX_RANGE = nautical_miles(100)

    def __init__(self, game: Game, transfer: TransferOrder) -> None:
        self.game = game
        self.transfer = transfer
        self.for_player = transfer.destination.captured
        self.package = Package(target=transfer.destination, auto_asap=True)

    def compatible_with_mission(
        self, unit_type: Type[FlyingType], airfield: ControlPoint
    ) -> bool:
        if not unit_type in TRANSPORT_CAPABLE:
            return False
        if not self.transfer.origin.can_operate(unit_type):
            return False
        if not self.transfer.destination.can_operate(unit_type):
            return False

        # Cargo planes have no maximum range.
        if not unit_type.helicopter:
            return True

        # A helicopter that is transport capable and able to operate at both bases. Need
        # to check that no leg of the journey exceeds the maximum range. This doesn't
        # account for any routing around threats that might take place, but it's close
        # enough.

        home = airfield.position
        pickup = self.transfer.position.position
        drop_off = self.transfer.position.position
        if meters(home.distance_to_point(pickup)) > self.HELO_MAX_RANGE:
            return False

        if meters(pickup.distance_to_point(drop_off)) > self.HELO_MAX_RANGE:
            return False

        if meters(drop_off.distance_to_point(home)) > self.HELO_MAX_RANGE:
            return False

        return True

    def create_package_for_airlift(self) -> None:
        distance_cache = ObjectiveDistanceCache.get_closest_airfields(
            self.transfer.position
        )
        for cp in distance_cache.closest_airfields:
            if cp.captured != self.for_player:
                continue

            inventory = self.game.aircraft_inventory.for_control_point(cp)
            for unit_type, available in inventory.all_aircraft:
                if self.compatible_with_mission(unit_type, cp):
                    while available and self.transfer.transport is None:
                        flight_size = self.create_airlift_flight(unit_type, inventory)
                        available -= flight_size
        if self.package.flights:
            self.game.ato_for(self.for_player).add_package(self.package)

    def create_airlift_flight(
        self, unit_type: Type[FlyingType], inventory: ControlPointAircraftInventory
    ) -> int:
        available = inventory.available(unit_type)
        # 4 is the max flight size in DCS.
        flight_size = min(self.transfer.size, available, 4)

        if flight_size < self.transfer.size:
            transfer = self.game.transfers.split_transfer(self.transfer, flight_size)
        else:
            transfer = self.transfer

        flight = Flight(
            self.package,
            self.game.player_country,
            unit_type,
            flight_size,
            FlightType.TRANSPORT,
            self.game.settings.default_start_type,
            departure=inventory.control_point,
            arrival=inventory.control_point,
            divert=None,
            cargo=transfer,
        )

        transport = Airlift(transfer, flight)
        transfer.transport = transport

        self.package.add_flight(flight)
        planner = FlightPlanBuilder(self.game, self.package, self.for_player)
        planner.populate_flight_plan(flight)
        self.game.aircraft_inventory.claim_for_flight(flight)
        return flight_size


class Convoy(MissionTarget, Transport):
    def __init__(self, origin: ControlPoint, destination: ControlPoint) -> None:
        super().__init__(namegen.next_convoy_name(), origin.position)
        self.origin = origin
        self.destination = destination
        self.transfers: List[TransferOrder] = []

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        if self.is_friendly(for_player):
            return

        yield FlightType.BAI
        yield from super().mission_types(for_player)

    def is_friendly(self, to_player: bool) -> bool:
        return self.origin.captured

    def add_units(self, transfer: TransferOrder) -> None:
        self.transfers.append(transfer)
        transfer.transport = self

    def remove_units(self, transfer: TransferOrder) -> None:
        transfer.transport = None
        self.transfers.remove(transfer)

    def kill_unit(self, unit_type: Type[VehicleType]) -> None:
        for transfer in self.transfers:
            try:
                transfer.kill_unit(unit_type)
                return
            except KeyError:
                pass
        raise KeyError

    def disband(self) -> None:
        for transfer in list(self.transfers):
            self.remove_units(transfer)
        self.transfers.clear()

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

    def find_escape_route(self) -> Optional[ControlPoint]:
        return None

    def description(self) -> str:
        return f"In a convoy to {self.destination}"

    @property
    def route_start(self) -> Point:
        return self.origin.convoy_spawns[self.destination]

    @property
    def route_end(self) -> Point:
        return self.destination.convoy_spawns[self.origin]


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
        self.convoys[convoy.origin][convoy.destination].disband()
        del self.convoys[convoy.origin][convoy.destination]

    @staticmethod
    def path_for(transfer: TransferOrder) -> List[ControlPoint]:
        supply_route = SupplyRoute.for_control_point(transfer.position)
        return supply_route.shortest_path_between(
            transfer.position, transfer.destination
        )

    def next_stop_for(self, transfer: TransferOrder) -> ControlPoint:
        return self.path_for(transfer)[0]

    def add(self, transfer: TransferOrder) -> None:
        next_stop = self.next_stop_for(transfer)
        self.find_or_create_convoy(transfer.position, next_stop).add_units(transfer)

    def remove(self, convoy: Convoy, transfer: TransferOrder) -> None:
        convoy.remove_units(transfer)
        if not convoy.transfers:
            self.disband_convoy(convoy)

    def disband_all(self) -> None:
        for convoy in list(self):
            self.disband_convoy(convoy)

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

    def arrange_transport(self, transfer: TransferOrder) -> None:
        supply_route = SupplyRoute.for_control_point(transfer.position)
        if transfer.destination in supply_route:
            self.convoys.add(transfer)
        else:
            AirliftPlanner(self.game, transfer).create_package_for_airlift()

    def new_transfer(self, transfer: TransferOrder) -> None:
        transfer.origin.base.commit_losses(transfer.units)
        self.pending_transfers.append(transfer)
        self.arrange_transport(transfer)

    def split_transfer(self, transfer: TransferOrder, size: int) -> TransferOrder:
        """Creates a smaller transfer that is a subset of the original."""
        if transfer.size <= size:
            raise ValueError

        units = {}
        for unit_type, remaining in transfer.units.items():
            take = min(remaining, size)
            size -= take
            transfer.units[unit_type] -= take
            units[unit_type] = take
            if not size:
                break
        new_transfer = TransferOrder(transfer.origin, transfer.destination, units)
        self.pending_transfers.append(new_transfer)
        return new_transfer

    @singledispatchmethod
    def cancel_transport(self, transfer: TransferOrder, transport) -> None:
        pass

    @cancel_transport.register
    def _cancel_transport_air(
        self, _transfer: TransferOrder, transport: Airlift
    ) -> None:
        flight = transport.flight
        flight.package.remove_flight(flight)
        self.game.aircraft_inventory.return_from_flight(flight)

    def _cancel_transport_convoy(
        self, transfer: TransferOrder, transport: Convoy
    ) -> None:
        self.convoys.remove(transport, transfer)

    def cancel_transfer(self, transfer: TransferOrder) -> None:
        if transfer.transport is not None:
            self.cancel_transport(transfer, transfer.transport)
        self.pending_transfers.remove(transfer)
        transfer.origin.base.commision_units(transfer.units)

    def perform_transfers(self) -> None:
        incomplete = []
        for transfer in self.pending_transfers:
            transfer.proceed()
            if not transfer.completed:
                incomplete.append(transfer)
        self.pending_transfers = incomplete
        self.convoys.disband_all()

    def plan_transports(self) -> None:
        for transfer in self.pending_transfers:
            if transfer.transport is None:
                self.arrange_transport(transfer)

    def order_airlift_assets(self) -> None:
        for control_point in self.game.theater.controlpoints:
            self.order_airlift_assets_at(control_point)

    @staticmethod
    def desired_airlift_capacity(control_point: ControlPoint) -> int:
        return 4 if control_point.has_factory else 0

    def current_airlift_capacity(self, control_point: ControlPoint) -> int:
        inventory = self.game.aircraft_inventory.for_control_point(control_point)
        return sum(
            count
            for unit_type, count in inventory.all_aircraft
            if unit_type in TRANSPORT_CAPABLE
        )

    def order_airlift_assets_at(self, control_point: ControlPoint) -> None:
        gap = self.desired_airlift_capacity(
            control_point
        ) - self.current_airlift_capacity(control_point)

        if gap <= 0:
            return

        if gap % 2:
            # Always buy in pairs since we're not trying to fill odd squadrons. Purely
            # aesthetic.
            gap += 1

        self.game.procurement_requests_for(player=control_point.captured).append(
            AircraftProcurementRequest(
                control_point, nautical_miles(200), FlightType.TRANSPORT, gap
            )
        )
