"""Implements support for ground unit transfers between bases.

Ground units can be transferred between bases via a number of transport methods, and
doing so can take multiple turns.

There are a few main concepts here:

* A TransferOrder is a request to move units from one base to another. It is described
  by its origin, destination, current position, and contents. TransferOrders persist
  across turns, and if no Transport is available to move the units in a given turn it
  will have no Transport assigned.
* Transports: A Transport is the planned move of a group of units for a leg of the
  journey *this turn*. A Transport has an assigned mode of transportation and has
  vehicles assigned to move the units if needed. This might be a Convoy, a CargoShip, or
  an Airlift.

The TransportMap (more accurately, it's subtypes) is responsible for managing the
transports moving from A to B for the turn. Transfers that are moving between A and B
this turn will be added to the TransportMap, which will create a new transport if needed
or add the units to an existing transport if one exists. This allows transfers from
A->B->C and D->B->C to share a transport between B and C.

AirLifts do not use TransportMap because no merging will take place between orders. It
instead uses AirLiftPlanner to create transport packages.

PendingTransfers manages all the incomplete transfer orders for the game. New transfer
orders are registered with PendingTransfers and it is responsible for allocating
transports and processing the turn's transit actions.

Routing is handled by TransitNetwork.
"""
from __future__ import annotations

import logging
import math
from collections import defaultdict
from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Generic, Iterator, List, Optional, Sequence, TYPE_CHECKING, TypeVar

from dcs.mapping import Point

from game.ato.ai_flight_planner_db import aircraft_for_task
from game.ato.closestairfields import ObjectiveDistanceCache
from game.ato.flight import Flight
from game.ato.flighttype import FlightType
from game.ato.package import Package
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.naming import namegen
from game.procurement import AircraftProcurementRequest
from game.theater import ControlPoint, MissionTarget
from game.theater.transitnetwork import (
    TransitConnection,
    TransitNetwork,
)
from game.utils import meters, nautical_miles

if TYPE_CHECKING:
    from game import Game
    from game.squadrons import Squadron


class Transport:
    def __init__(self, destination: ControlPoint):
        self.destination = destination

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
    units: dict[GroundUnitType, int]

    transport: Optional[Transport] = field(default=None)

    request_airflift: bool = field(default=False)

    def __str__(self) -> str:
        """Returns the text that should be displayed for the transfer."""
        count = self.size
        origin = self.origin.name
        destination = self.destination.name
        description = "Transfer" if self.player else "Enemy transfer"
        return f"{description} of {count} units from {origin} to {destination}"

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

    def kill_unit(self, unit_type: GroundUnitType) -> None:
        if unit_type not in self.units or not self.units[unit_type]:
            raise KeyError(f"{self} has no {unit_type} remaining")
        if self.units[unit_type] == 1:
            del self.units[unit_type]
        else:
            self.units[unit_type] -= 1

    @property
    def size(self) -> int:
        return sum(self.units.values())

    def iter_units(self) -> Iterator[GroundUnitType]:
        for unit_type, count in self.units.items():
            for _ in range(count):
                yield unit_type

    @property
    def completed(self) -> bool:
        return self.destination == self.position or not self.size

    def disband_at(self, location: ControlPoint) -> None:
        logging.info(f"Units halting at {location}.")
        location.base.commission_units(self.units)
        self.units.clear()

    @property
    def next_stop(self) -> ControlPoint:
        if self.transport is None:
            raise RuntimeError(
                "TransferOrder.next_stop called with no transport assigned"
            )
        return self.transport.destination

    def find_escape_route(self) -> Optional[ControlPoint]:
        if self.transport is not None:
            return self.transport.find_escape_route()
        return None

    def disband(self) -> None:
        """
        Disbands the specific transfer at the current position if friendly, at a
        possible escape route or kills all units if none is possible
        """
        if self.position.is_friendly(self.player):
            self.disband_at(self.position)
        elif (escape_route := self.find_escape_route()) is not None:
            self.disband_at(escape_route)
        else:
            logging.info(
                f"No escape route available. Units were surrounded and destroyed "
                "during transfer."
            )
            self.kill_all()

    def is_completable(self, network: TransitNetwork) -> bool:
        """
        Checks if the transfer can be completed with the current theater state / transit
        network to ensure that there is possible route between the current position and
        the planned destination. This also ensures that the points are friendly.
        """
        if self.transport is None:
            # Check if unplanned transfers could be completed
            if not self.position.is_friendly(self.player):
                logging.info(
                    f"Current position ({self.position}) "
                    f"of the halting transfer was captured."
                )
                return False
            if not network.has_path_between(self.position, self.destination):
                logging.info(
                    f"Destination of transfer ({self.destination}) "
                    f"can not be reached anymore."
                )
                return False

        if self.transport is not None and not self.next_stop.is_friendly(self.player):
            # check if already proceeding transfers can reach the next stop
            logging.info(
                f"The next stop of the transfer ({self.next_stop}) "
                f"was captured while transfer was on route."
            )
            return False

        return True

    def proceed(self) -> None:
        """
        Let the transfer proceed to the next stop and disbands it if the next stop
        is the destination
        """
        if self.transport is None:
            return

        self.position = self.next_stop
        self.transport = None

        if self.completed:
            self.disband_at(self.position)


class Airlift(Transport):
    """A transfer order that moves units by cargo planes and helicopters."""

    def __init__(
        self, transfer: TransferOrder, flight: Flight, next_stop: ControlPoint
    ) -> None:
        super().__init__(next_stop)
        self.transfer = transfer
        self.flight = flight

    @property
    def units(self) -> dict[GroundUnitType, int]:
        return self.transfer.units

    @property
    def player_owned(self) -> bool:
        return self.transfer.player

    def find_escape_route(self) -> Optional[ControlPoint]:
        # TODO: Move units to closest base.
        return None

    def description(self) -> str:
        return (
            f"Being airlifted from {self.transfer.position} to {self.destination} by "
            f"{self.flight}"
        )


class AirliftPlanner:
    #: Maximum range from for any link in the route of takeoff, pickup, dropoff, and RTB
    #: for a helicopter to be considered for airlift. Total route length is not
    #: considered because the helicopter can refuel at each stop. Cargo planes have no
    #: maximum range.
    HELO_MAX_RANGE = nautical_miles(100)

    def __init__(
        self, game: Game, transfer: TransferOrder, next_stop: ControlPoint
    ) -> None:
        self.game = game
        self.transfer = transfer
        self.next_stop = next_stop
        self.for_player = transfer.destination.captured
        self.package = Package(next_stop, game.db.flights, auto_asap=True)

    def compatible_with_mission(
        self, unit_type: AircraftType, airfield: ControlPoint
    ) -> bool:
        if unit_type not in aircraft_for_task(FlightType.TRANSPORT):
            return False
        if not self.transfer.origin.can_operate(unit_type):
            return False
        if not self.next_stop.can_operate(unit_type):
            return False

        # Cargo planes have no maximum range.
        if not unit_type.dcs_unit_type.helicopter:
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
        air_wing = self.game.air_wing_for(self.for_player)
        for cp in distance_cache.closest_airfields:
            if cp.captured != self.for_player:
                continue

            squadrons = air_wing.auto_assignable_for_task_at(FlightType.TRANSPORT, cp)
            for squadron in squadrons:
                if self.compatible_with_mission(squadron.aircraft, cp):
                    while (
                        squadron.untasked_aircraft
                        and squadron.has_available_pilots
                        and self.transfer.transport is None
                    ):
                        self.create_airlift_flight(squadron)
        if self.package.flights:
            self.package.set_tot_asap()
            self.game.ato_for(self.for_player).add_package(self.package)

    def create_airlift_flight(self, squadron: Squadron) -> int:
        available_aircraft = squadron.untasked_aircraft
        capacity_each = 1 if squadron.aircraft.dcs_unit_type.helicopter else 2
        required = math.ceil(self.transfer.size / capacity_each)
        flight_size = min(
            required,
            available_aircraft,
            squadron.aircraft.dcs_unit_type.group_size_max,
        )
        # TODO: Use number_of_available_pilots directly once feature flag is gone.
        # The number of currently available pilots is not relevant when pilot limits
        # are disabled.
        if not squadron.can_fulfill_flight(flight_size):
            flight_size = squadron.max_fulfillable_aircraft
        capacity = flight_size * capacity_each

        if capacity < self.transfer.size:
            transfer = self.game.coalition_for(
                self.for_player
            ).transfers.split_transfer(self.transfer, capacity)
        else:
            transfer = self.transfer

        start_type = squadron.location.required_aircraft_start_type
        if start_type is None:
            start_type = self.game.settings.default_start_type

        flight = Flight(
            self.package,
            self.game.country_for(squadron.player),
            squadron,
            flight_size,
            FlightType.TRANSPORT,
            start_type,
            divert=None,
            cargo=transfer,
        )

        transport = Airlift(transfer, flight, self.next_stop)
        transfer.transport = transport

        self.package.add_flight(flight)
        flight.recreate_flight_plan()
        return flight_size


class MultiGroupTransport(MissionTarget, Transport):
    def __init__(
        self, name: str, origin: ControlPoint, destination: ControlPoint
    ) -> None:
        MissionTarget.__init__(self, name, origin.position)
        Transport.__init__(self, destination)
        self.origin = origin
        self.transfers: List[TransferOrder] = []

    def is_friendly(self, to_player: bool) -> bool:
        return self.origin.captured

    def add_units(self, transfer: TransferOrder) -> None:
        self.transfers.append(transfer)
        transfer.transport = self

    def remove_units(self, transfer: TransferOrder) -> None:
        transfer.transport = None
        self.transfers.remove(transfer)

    def kill_unit(self, unit_type: GroundUnitType) -> None:
        for transfer in self.transfers:
            try:
                transfer.kill_unit(unit_type)
                return
            except KeyError:
                pass
        raise KeyError

    def kill_all(self) -> None:
        for transfer in self.transfers:
            transfer.kill_all()

    def disband(self) -> None:
        for transfer in list(self.transfers):
            self.remove_units(transfer)
        self.transfers.clear()

    @property
    def size(self) -> int:
        return sum(t.size for t in self.transfers)

    @property
    def units(self) -> dict[GroundUnitType, int]:
        units: dict[GroundUnitType, int] = defaultdict(int)
        for transfer in self.transfers:
            for unit_type, count in transfer.units.items():
                units[unit_type] += count
        return units

    def iter_units(self) -> Iterator[GroundUnitType]:
        for unit_type, count in self.units.items():
            for _ in range(count):
                yield unit_type

    @property
    def player_owned(self) -> bool:
        return self.origin.captured

    def find_escape_route(self) -> Optional[ControlPoint]:
        raise NotImplementedError

    def description(self) -> str:
        raise NotImplementedError


class Convoy(MultiGroupTransport):
    def __init__(self, origin: ControlPoint, destination: ControlPoint) -> None:
        super().__init__(namegen.next_convoy_name(), origin, destination)

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        if self.is_friendly(for_player):
            return

        yield FlightType.BAI
        yield from super().mission_types(for_player)

    @property
    def route_start(self) -> Point:
        return self.origin.convoy_origin_for(self.destination)

    @property
    def route_end(self) -> Point:
        return self.destination.convoy_origin_for(self.origin)

    def description(self) -> str:
        return f"In a convoy from {self.origin} to {self.destination}"

    def find_escape_route(self) -> Optional[ControlPoint]:
        return None


class CargoShip(MultiGroupTransport):
    def __init__(self, origin: ControlPoint, destination: ControlPoint) -> None:
        super().__init__(namegen.next_cargo_ship_name(), origin, destination)

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        if self.is_friendly(for_player):
            return

        yield FlightType.ANTISHIP
        yield from super().mission_types(for_player)

    @property
    def route(self) -> Sequence[Point]:
        return self.origin.shipping_lanes[self.destination]

    def description(self) -> str:
        return f"On a ship from {self.origin} to {self.destination}"

    def find_escape_route(self) -> Optional[ControlPoint]:
        return None


TransportType = TypeVar("TransportType", bound=MultiGroupTransport)


class TransportMap(Generic[TransportType]):
    def __init__(self) -> None:
        # Dict of origin -> destination -> transport.
        self.transports: dict[
            ControlPoint, dict[ControlPoint, TransportType]
        ] = defaultdict(dict)

    def create_transport(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> TransportType:
        raise NotImplementedError

    def transport_exists(self, origin: ControlPoint, destination: ControlPoint) -> bool:
        return destination in self.transports[origin]

    def find_transport(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> Optional[TransportType]:
        return self.transports[origin].get(destination)

    def find_or_create_transport(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> TransportType:
        transport = self.find_transport(origin, destination)
        if transport is None:
            transport = self.create_transport(origin, destination)
            self.transports[origin][destination] = transport
        return transport

    def departing_from(self, origin: ControlPoint) -> Iterator[TransportType]:
        yield from self.transports[origin].values()

    def travelling_to(self, destination: ControlPoint) -> Iterator[TransportType]:
        for destination_dict in self.transports.values():
            if destination in destination_dict:
                yield destination_dict[destination]

    def disband_transport(self, transport: TransportType) -> None:
        transport.disband()
        del self.transports[transport.origin][transport.destination]

    def add(self, transfer: TransferOrder, next_stop: ControlPoint) -> None:
        self.find_or_create_transport(transfer.position, next_stop).add_units(transfer)

    def remove(self, transport: TransportType, transfer: TransferOrder) -> None:
        transport.remove_units(transfer)
        if not transport.transfers:
            self.disband_transport(transport)

    def disband_all(self) -> None:
        for transport in list(self):
            self.disband_transport(transport)

    def __iter__(self) -> Iterator[TransportType]:
        for destination_dict in self.transports.values():
            yield from destination_dict.values()


class ConvoyMap(TransportMap[Convoy]):
    def create_transport(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> Convoy:
        return Convoy(origin, destination)


class CargoShipMap(TransportMap[CargoShip]):
    def create_transport(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> CargoShip:
        return CargoShip(origin, destination)


class PendingTransfers:
    def __init__(self, game: Game, player: bool) -> None:
        self.game = game
        self.player = player
        self.convoys = ConvoyMap()
        self.cargo_ships = CargoShipMap()
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

    def network_for(self, control_point: ControlPoint) -> TransitNetwork:
        return self.game.transit_network_for(control_point.captured)

    def arrange_transport(self, transfer: TransferOrder) -> None:
        network = self.network_for(transfer.position)
        path = network.shortest_path_between(transfer.position, transfer.destination)
        next_stop = path[0]
        if not transfer.request_airflift:
            if (
                network.link_type(transfer.position, next_stop)
                == TransitConnection.Road
            ):
                return self.convoys.add(transfer, next_stop)
            elif (
                network.link_type(transfer.position, next_stop)
                == TransitConnection.Shipping
            ):
                return self.cargo_ships.add(transfer, next_stop)
        AirliftPlanner(self.game, transfer, next_stop).create_package_for_airlift()

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

    # Type checking ignored because singledispatchmethod doesn't work with required type
    # definitions. The implementation methods are all typed, so should be fine.
    @singledispatchmethod
    def cancel_transport(  # type: ignore
        self,
        transport,
        transfer: TransferOrder,
    ) -> None:
        pass

    @cancel_transport.register
    def _cancel_transport_air(
        self, transport: Airlift, _transfer: TransferOrder
    ) -> None:
        flight = transport.flight
        flight.package.remove_flight(flight)
        if not flight.package.flights:
            self.game.ato_for(self.player).remove_package(flight.package)

    @cancel_transport.register
    def _cancel_transport_convoy(
        self, transport: Convoy, transfer: TransferOrder
    ) -> None:
        self.convoys.remove(transport, transfer)

    @cancel_transport.register
    def _cancel_transport_cargo_ship(
        self, transport: CargoShip, transfer: TransferOrder
    ) -> None:
        self.cargo_ships.remove(transport, transfer)

    def cancel_transfer(self, transfer: TransferOrder) -> None:
        if transfer.transport is not None:
            self.cancel_transport(transfer.transport, transfer)
        self.pending_transfers.remove(transfer)
        transfer.origin.base.commission_units(transfer.units)

    def perform_transfers(self) -> None:
        """
        Performs completable transfers from the list of pending transfers and adds
        uncompleted transfers which are en route back to the list of pending transfers.
        Disbands all convoys and cargo ships
        """
        self.disband_uncompletable_transfers()
        incomplete = []
        for transfer in self.pending_transfers:
            transfer.proceed()
            if not transfer.completed:
                incomplete.append(transfer)
        self.pending_transfers = incomplete
        self.convoys.disband_all()
        self.cargo_ships.disband_all()

    def plan_transports(self) -> None:
        """
        Plan transports for all pending and completable transfers which don't have a
        transport assigned already. This calculates the shortest path between current
        position and destination on every execution to ensure the route is adopted to
        recent changes in the theater state / transit network.
        """
        self.disband_uncompletable_transfers()
        for transfer in self.pending_transfers:
            if transfer.transport is None:
                self.arrange_transport(transfer)

    def disband_uncompletable_transfers(self) -> None:
        """
        Disbands all transfers from the list of pending_transfers which can not be
        completed anymore because the theater state changed or the transit network does
        not allow a route to the destination anymore
        """
        completable_transfers = []
        for transfer in self.pending_transfers:
            if not transfer.is_completable(self.network_for(transfer.position)):
                if transfer.transport:
                    self.cancel_transport(transfer.transport, transfer)
                transfer.disband()
            else:
                completable_transfers.append(transfer)
        self.pending_transfers = completable_transfers

    def order_airlift_assets(self) -> None:
        for control_point in self.game.theater.control_points_for(self.player):
            if self.game.air_wing_for(control_point.captured).can_auto_plan(
                FlightType.TRANSPORT
            ):
                self.order_airlift_assets_at(control_point)

    def desired_airlift_capacity(self, control_point: ControlPoint) -> int:

        if control_point.has_factory:
            is_major_hub = control_point.total_aircraft_parking > 0
            # Check if there is a CP which is only reachable via Airlift
            transit_network = self.network_for(control_point)
            for cp in self.game.theater.control_points_for(self.player):
                # check if the CP has no factory, is reachable from the current
                # position and can only be reached with airlift connections
                if (
                    cp.can_deploy_ground_units
                    and not cp.has_factory
                    and transit_network.has_link(control_point, cp)
                    and not any(
                        link_type
                        for link, link_type in transit_network.nodes[cp].items()
                        if not link_type == TransitConnection.Airlift
                    )
                ):
                    return 4

                if (
                    is_major_hub
                    and cp.has_factory
                    and cp.total_aircraft_parking > control_point.total_aircraft_parking
                ):
                    is_major_hub = False

            if is_major_hub:
                # If the current CP is a major hub keep always 2 planes on reserve
                return 2

        return 0

    @staticmethod
    def current_airlift_capacity(control_point: ControlPoint) -> int:
        return sum(
            s.owned_aircraft
            for s in control_point.squadrons
            if s.can_auto_assign(FlightType.TRANSPORT)
        )

    def order_airlift_assets_at(self, control_point: ControlPoint) -> None:
        unclaimed_parking = control_point.unclaimed_parking()
        # Buy a maximum of unclaimed_parking only to prevent that aircraft procurement
        # take place at another base
        gap = min(
            [
                self.desired_airlift_capacity(control_point)
                - self.current_airlift_capacity(control_point),
                unclaimed_parking,
            ]
        )

        if gap <= 0:
            return

        if gap % 2:
            # Always buy in pairs since we're not trying to fill odd squadrons. Purely
            # aesthetic.
            gap += 1

        if gap > unclaimed_parking:
            # Prevent to buy more aircraft than possible
            return

        self.game.coalition_for(self.player).add_procurement_request(
            AircraftProcurementRequest(control_point, FlightType.TRANSPORT, gap)
        )

    def transfer_for_flight(self, flight: Flight) -> Optional[TransferOrder]:
        for transfer in self.pending_transfers:
            if transfer.transport is None or not isinstance(
                transfer.transport, Airlift
            ):
                continue
            if transfer.transport.flight == flight:
                return transfer
        return None
