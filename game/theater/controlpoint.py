from __future__ import annotations

import heapq
import itertools
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, unique, auto, IntEnum
from functools import total_ordering, cached_property
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    TYPE_CHECKING,
    Type,
    Union,
    Sequence,
    Iterable,
    Tuple,
)

from dcs.mapping import Point
from dcs.ships import (
    CVN_74_John_C__Stennis,
    CV_1143_5_Admiral_Kuznetsov,
    LHA_1_Tarawa,
    Type_071_Amphibious_Transport_Dock,
)
from dcs.terrain.terrain import Airport, ParkingSlot
from dcs.unit import Unit
from dcs.unittype import FlyingType, VehicleType

from game import db
from game.point_with_heading import PointWithHeading
from game.scenery_group import SceneryGroup
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.ground_forces.combat_stance import CombatStance
from gen.runways import RunwayAssigner, RunwayData
from .base import Base
from .missiontarget import MissionTarget
from .theatergroundobject import (
    GenericCarrierGroundObject,
    TheaterGroundObject,
)
from ..db import PRICES
from ..utils import nautical_miles
from ..weather import Conditions

if TYPE_CHECKING:
    from game import Game
    from gen.flights.flight import FlightType
    from ..transfers import PendingTransfers

FREE_FRONTLINE_UNIT_SUPPLY: int = 15
AMMO_DEPOT_FRONTLINE_UNIT_CONTRIBUTION: int = 12


class ControlPointType(Enum):
    #: An airbase with slots for everything.
    AIRBASE = 0
    #: A group with a Stennis type carrier (F/A-18, F-14 compatible).
    AIRCRAFT_CARRIER_GROUP = 1
    #: A group with a Tarawa carrier (Helicopters & Harrier).
    LHA_GROUP = 2
    #: A FARP, with slots for helicopters
    FARP = 4
    #: A FOB (ground units only)
    FOB = 5
    OFF_MAP = 6


@dataclass
class PresetLocations:
    """Defines the preset locations loaded from the campaign mission file."""

    #: Locations used by non-carrier ships that will be spawned unless the faction has
    #: no navy or the player has disabled ship generation for the owning side.
    ships: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by coastal defenses that are generated if the faction is capable.
    coastal_defenses: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by ground based strike objectives.
    strike_locations: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by offshore strike objectives.
    offshore_strike_locations: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by missile sites like scuds and V-2s that are generated if the
    #: faction is capable.
    missile_sites: List[PointWithHeading] = field(default_factory=list)

    #: Locations of long range SAMs.
    long_range_sams: List[PointWithHeading] = field(default_factory=list)

    #: Locations of medium range SAMs.
    medium_range_sams: List[PointWithHeading] = field(default_factory=list)

    #: Locations of short range SAMs.
    short_range_sams: List[PointWithHeading] = field(default_factory=list)

    #: Locations of AAA groups.
    aaa: List[PointWithHeading] = field(default_factory=list)

    #: Locations of EWRs.
    ewrs: List[PointWithHeading] = field(default_factory=list)

    #: Locations of map scenery to create zones for.
    scenery: List[SceneryGroup] = field(default_factory=list)

    #: Locations of factories for producing ground units.
    factories: List[PointWithHeading] = field(default_factory=list)

    #: Locations of ammo depots for controlling number of units on the front line at a
    #: control point.
    ammunition_depots: List[PointWithHeading] = field(default_factory=list)

    #: Locations of stationary armor groups.
    armor_groups: List[PointWithHeading] = field(default_factory=list)


@dataclass(frozen=True)
class AircraftAllocations:
    present: dict[Type[FlyingType], int]
    ordered: dict[Type[FlyingType], int]
    transferring: dict[Type[FlyingType], int]

    @property
    def total_value(self) -> int:
        total: int = 0
        for unit_type, count in self.present.items():
            total += PRICES[unit_type] * count
        for unit_type, count in self.ordered.items():
            total += PRICES[unit_type] * count
        for unit_type, count in self.transferring.items():
            total += PRICES[unit_type] * count

        return total

    @property
    def total(self) -> int:
        return self.total_present + self.total_ordered + self.total_transferring

    @property
    def total_present(self) -> int:
        return sum(self.present.values())

    @property
    def total_ordered(self) -> int:
        return sum(self.ordered.values())

    @property
    def total_transferring(self) -> int:
        return sum(self.transferring.values())


@dataclass(frozen=True)
class GroundUnitAllocations:
    present: dict[Type[VehicleType], int]
    ordered: dict[Type[VehicleType], int]
    transferring: dict[Type[VehicleType], int]

    @property
    def all(self) -> dict[Type[VehicleType], int]:
        combined: dict[Type[VehicleType], int] = defaultdict(int)
        for unit_type, count in itertools.chain(
            self.present.items(), self.ordered.items(), self.transferring.items()
        ):
            combined[unit_type] += count
        return dict(combined)

    @property
    def total_value(self) -> int:
        total: int = 0
        for unit_type, count in self.present.items():
            total += PRICES[unit_type] * count
        for unit_type, count in self.ordered.items():
            total += PRICES[unit_type] * count
        for unit_type, count in self.transferring.items():
            total += PRICES[unit_type] * count

        return total

    @cached_property
    def total(self) -> int:
        return self.total_present + self.total_ordered + self.total_transferring

    @cached_property
    def total_present(self) -> int:
        return sum(self.present.values())

    @cached_property
    def total_ordered(self) -> int:
        return sum(self.ordered.values())

    @cached_property
    def total_transferring(self) -> int:
        return sum(self.transferring.values())


@dataclass
class RunwayStatus:
    damaged: bool = False
    repair_turns_remaining: Optional[int] = None

    def damage(self) -> None:
        self.damaged = True
        # If the runway is already under repair and is damaged again, progress
        # is reset.
        self.repair_turns_remaining = None

    def begin_repair(self) -> None:
        if self.repair_turns_remaining is not None:
            logging.error("Runway already under repair. Restarting.")
        self.repair_turns_remaining = 4

    def process_turn(self) -> None:
        if self.repair_turns_remaining is not None:
            if self.repair_turns_remaining == 1:
                self.repair_turns_remaining = None
                self.damaged = False
            else:
                self.repair_turns_remaining -= 1

    @property
    def needs_repair(self) -> bool:
        return self.damaged and self.repair_turns_remaining is None

    def __str__(self) -> str:
        if not self.damaged:
            return "Runway operational"

        turns_remaining = self.repair_turns_remaining
        if turns_remaining is None:
            return "Runway damaged"

        return f"Runway repairing, {turns_remaining} turns remaining"


@total_ordering
class GroundUnitDestination:
    def __init__(self, control_point: ControlPoint) -> None:
        self.control_point = control_point

    @property
    def total_value(self) -> float:
        return self.control_point.base.total_armor_value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GroundUnitDestination):
            raise TypeError

        return self.total_value == other.total_value

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, GroundUnitDestination):
            raise TypeError

        return self.total_value < other.total_value


@unique
class ControlPointStatus(IntEnum):
    Functional = auto()
    Damaged = auto()
    Destroyed = auto()


class ControlPoint(MissionTarget, ABC):

    position = None  # type: Point
    name = None  # type: str

    captured = False
    has_frontline = True

    alt = 0

    # TODO: Only airbases have IDs.
    # TODO: has_frontline is only reasonable for airbases.
    # TODO: cptype is obsolete.
    def __init__(
        self,
        cp_id: int,
        name: str,
        position: Point,
        at: db.StartingPosition,
        size: int,
        importance: float,
        has_frontline=True,
        cptype=ControlPointType.AIRBASE,
    ):
        super().__init__(name, position)
        # TODO: Should be Airbase specific.
        self.id = cp_id
        self.full_name = name
        self.at = at
        self.connected_objectives: List[TheaterGroundObject] = []
        self.preset_locations = PresetLocations()
        self.helipads: List[PointWithHeading] = []

        # TODO: Should be Airbase specific.
        self.size = size
        self.importance = importance
        self.captured = False
        self.captured_invert = False
        # TODO: Should be Airbase specific.
        self.has_frontline = has_frontline
        self.connected_points: List[ControlPoint] = []
        self.convoy_routes: Dict[ControlPoint, Tuple[Point, ...]] = {}
        self.shipping_lanes: Dict[ControlPoint, Tuple[Point, ...]] = {}
        self.base: Base = Base()
        self.cptype = cptype
        # TODO: Should be Airbase specific.
        self.stances: Dict[int, CombatStance] = {}
        from ..unitdelivery import PendingUnitDeliveries

        self.pending_unit_deliveries = PendingUnitDeliveries(self)

        self.target_position: Optional[Point] = None

    def __repr__(self):
        return f"<{__class__}: {self.name}>"

    @property
    def ground_objects(self) -> List[TheaterGroundObject]:
        return list(self.connected_objectives)

    @property
    @abstractmethod
    def heading(self) -> int:
        ...

    def __str__(self):
        return self.name

    @property
    def is_global(self):
        return not self.connected_points

    def transitive_connected_friendly_points(
        self, seen: Optional[Set[ControlPoint]] = None
    ) -> List[ControlPoint]:
        if seen is None:
            seen = {self}

        connected = []
        for cp in self.connected_points:
            if cp.captured != self.captured:
                continue
            if cp in seen:
                continue
            seen.add(cp)
            connected.append(cp)
            connected.extend(cp.transitive_connected_friendly_points(seen))
        return connected

    def transitive_friendly_shipping_destinations(
        self, seen: Optional[Set[ControlPoint]] = None
    ) -> List[ControlPoint]:
        if seen is None:
            seen = {self}

        connected = []
        for cp in self.shipping_lanes:
            if cp.captured != self.captured:
                continue
            if cp in seen:
                continue
            seen.add(cp)
            connected.append(cp)
            connected.extend(cp.transitive_friendly_shipping_destinations(seen))
        return connected

    @property
    def has_factory(self) -> bool:
        for tgo in self.connected_objectives:
            if tgo.is_factory and not tgo.is_dead:
                return True
        return False

    def can_recruit_ground_units(self, game: Game) -> bool:
        """Returns True if this control point is capable of recruiting ground units."""
        if not self.can_deploy_ground_units:
            return False

        if game.turn == 0:
            # Allow units to be recruited anywhere on turn 0 to avoid long delays to get
            # everyone to the front line.
            return True

        return self.has_factory

    def has_ground_unit_source(self, game: Game) -> bool:
        """Returns True if this control point has access to ground reinforcements."""
        if not self.can_deploy_ground_units:
            return False

        for cp in game.theater.controlpoints:
            if cp.is_friendly(self.captured) and cp.can_recruit_ground_units(game):
                return True
        return False

    @property
    def is_carrier(self):
        """
        :return: Whether this control point is an aircraft carrier
        """
        return False

    @property
    def is_fleet(self):
        """
        :return: Whether this control point is a boat (mobile)
        """
        return False

    @property
    def is_lha(self):
        """
        :return: Whether this control point is an LHA
        """
        return False

    @property
    def moveable(self) -> bool:
        """
        :return: Whether this control point can be moved around
        """
        return False

    @property
    @abstractmethod
    def can_deploy_ground_units(self) -> bool:
        ...

    @property
    @abstractmethod
    def total_aircraft_parking(self):
        """
        :return: The maximum number of aircraft that can be stored in this
                 control point
        """
        ...

    def convoy_origin_for(self, destination: ControlPoint) -> Point:
        return self.convoy_route_to(destination)[0]

    def convoy_route_to(self, destination: ControlPoint) -> Sequence[Point]:
        return self.convoy_routes[destination]

    def create_convoy_route(self, to: ControlPoint, waypoints: Iterable[Point]) -> None:
        self.connected_points.append(to)
        self.stances[to.id] = CombatStance.DEFENSIVE
        self.convoy_routes[to] = tuple(waypoints)

    def create_shipping_lane(
        self, to: ControlPoint, waypoints: Iterable[Point]
    ) -> None:
        self.shipping_lanes[to] = tuple(waypoints)

    @abstractmethod
    def runway_is_operational(self) -> bool:
        """
        Check whether this control point supports taking offs and landings.
        :return:
        """
        ...

    # TODO: Should be naval specific.
    def get_carrier_group_name(self):
        """
        Get the carrier group name if the airbase is a carrier
        :return: Carrier group name
        """
        if self.cptype in [
            ControlPointType.AIRCRAFT_CARRIER_GROUP,
            ControlPointType.LHA_GROUP,
        ]:
            for g in self.ground_objects:
                if g.dcs_identifier == "CARRIER":
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [
                                CVN_74_John_C__Stennis,
                                CV_1143_5_Admiral_Kuznetsov,
                            ]:
                                return group.name
                elif g.dcs_identifier == "LHA":
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [LHA_1_Tarawa]:
                                return group.name
        return None

    # TODO: Should be Airbase specific.
    def is_connected(self, to) -> bool:
        return to in self.connected_points

    def find_ground_objects_by_obj_name(self, obj_name):
        found = []
        for g in self.ground_objects:
            if g.obj_name == obj_name:
                found.append(g)
        return found

    def is_friendly(self, to_player: bool) -> bool:
        return self.captured == to_player

    def is_friendly_to(self, control_point: ControlPoint) -> bool:
        return control_point.is_friendly(self.captured)

    def capture_equipment(self, game: Game) -> None:
        total = self.base.total_armor_value
        self.base.armor.clear()
        game.adjust_budget(total, player=not self.captured)
        game.message(
            f"{self.name} is not connected to any friendly points. Ground "
            f"vehicles have been captured and sold for ${total}M."
        )

    def retreat_ground_units(self, game: Game):
        # When there are multiple valid destinations, deliver units to whichever
        # base is least defended first. The closest approximation of unit
        # strength we have is price
        destinations = [
            GroundUnitDestination(cp)
            for cp in self.connected_points
            if cp.captured == self.captured
        ]
        if not destinations:
            self.capture_equipment(game)
            return

        heapq.heapify(destinations)
        destination = heapq.heappop(destinations)
        while self.base.armor:
            unit_type, count = self.base.armor.popitem()
            for _ in range(count):
                destination.control_point.base.commission_units({unit_type: 1})
                destination = heapq.heappushpop(destinations, destination)

    def capture_aircraft(
        self, game: Game, airframe: Type[FlyingType], count: int
    ) -> None:
        try:
            value = PRICES[airframe] * count
        except KeyError:
            logging.exception(f"Unknown price for {airframe.id}")
            return

        game.adjust_budget(value, player=not self.captured)
        game.message(
            f"No valid retreat destination in range of {self.name} for "
            f"{airframe.id}. {count} aircraft have been captured and sold for "
            f"${value}M."
        )

    def aircraft_retreat_destination(
        self, game: Game, airframe: Type[FlyingType]
    ) -> Optional[ControlPoint]:
        closest = ObjectiveDistanceCache.get_closest_airfields(self)
        # TODO: Should be airframe dependent.
        max_retreat_distance = nautical_miles(200)
        # Skip the first airbase because that's the airbase we're retreating
        # from.
        airfields = list(closest.operational_airfields_within(max_retreat_distance))[1:]
        for airbase in airfields:
            if not airbase.can_operate(airframe):
                continue
            if airbase.captured != self.captured:
                continue
            if airbase.unclaimed_parking(game) > 0:
                return airbase
        return None

    def _retreat_air_units(
        self, game: Game, airframe: Type[FlyingType], count: int
    ) -> None:
        while count:
            logging.debug(f"Retreating {count} {airframe.id} from {self.name}")
            destination = self.aircraft_retreat_destination(game, airframe)
            if destination is None:
                self.capture_aircraft(game, airframe, count)
                return
            parking = destination.unclaimed_parking(game)
            transfer_amount = min([parking, count])
            destination.base.commission_units({airframe: transfer_amount})
            count -= transfer_amount

    def retreat_air_units(self, game: Game) -> None:
        # TODO: Capture in order of price to retain maximum value?
        while self.base.aircraft:
            airframe, count = self.base.aircraft.popitem()
            self._retreat_air_units(game, airframe, count)

    def depopulate_uncapturable_tgos(self) -> None:
        for tgo in self.connected_objectives:
            if not tgo.capturable:
                tgo.clear()

    # TODO: Should be Airbase specific.
    def capture(self, game: Game, for_player: bool) -> None:
        self.pending_unit_deliveries.refund_all(game)
        self.retreat_ground_units(game)
        self.retreat_air_units(game)
        self.depopulate_uncapturable_tgos()

        if for_player:
            self.captured = True
        else:
            self.captured = False

        self.base.set_strength_to_minimum()

    @abstractmethod
    def can_operate(self, aircraft: Type[FlyingType]) -> bool:
        ...

    def aircraft_transferring(self, game: Game) -> dict[Type[FlyingType], int]:
        if self.captured:
            ato = game.blue_ato
        else:
            ato = game.red_ato

        transferring: defaultdict[Type[FlyingType], int] = defaultdict(int)
        for package in ato.packages:
            for flight in package.flights:
                if flight.departure == flight.arrival:
                    continue
                if flight.departure == self:
                    transferring[flight.unit_type] -= flight.count
                elif flight.arrival == self:
                    transferring[flight.unit_type] += flight.count
        return transferring

    def unclaimed_parking(self, game: Game) -> int:
        return self.total_aircraft_parking - self.allocated_aircraft(game).total

    @abstractmethod
    def active_runway(
        self, conditions: Conditions, dynamic_runways: Dict[str, RunwayData]
    ) -> RunwayData:
        ...

    @property
    def parking_slots(self) -> Iterator[ParkingSlot]:
        yield from []

    @property
    @abstractmethod
    def runway_status(self) -> RunwayStatus:
        ...

    @property
    def runway_can_be_repaired(self) -> bool:
        return self.runway_status.needs_repair

    def begin_runway_repair(self) -> None:
        if not self.runway_can_be_repaired:
            logging.error(f"Cannot repair runway at {self}")
            return
        self.runway_status.begin_repair()

    def process_turn(self, game: Game) -> None:
        self.pending_unit_deliveries.process(game)

        runway_status = self.runway_status
        if runway_status is not None:
            runway_status.process_turn()

        # Process movements for ships control points group
        if self.target_position is not None:
            delta = self.target_position - self.position
            self.position = self.target_position
            self.target_position = None

            # Move the linked unit groups
            for ground_object in self.ground_objects:
                if isinstance(ground_object, GenericCarrierGroundObject):
                    ground_object.position.x = ground_object.position.x + delta.x
                    ground_object.position.y = ground_object.position.y + delta.y
                    for group in ground_object.groups:
                        for u in group.units:
                            u.position.x = u.position.x + delta.x
                            u.position.y = u.position.y + delta.y

    def allocated_aircraft(self, game: Game) -> AircraftAllocations:
        on_order = {}
        for unit_bought, count in self.pending_unit_deliveries.units.items():
            if issubclass(unit_bought, FlyingType):
                on_order[unit_bought] = count

        return AircraftAllocations(
            self.base.aircraft, on_order, self.aircraft_transferring(game)
        )

    def allocated_ground_units(
        self, transfers: PendingTransfers
    ) -> GroundUnitAllocations:
        on_order = {}
        for unit_bought, count in self.pending_unit_deliveries.units.items():
            if issubclass(unit_bought, VehicleType):
                on_order[unit_bought] = count

        transferring: dict[Type[VehicleType], int] = defaultdict(int)
        for transfer in transfers:
            if transfer.destination == self:
                for unit_type, count in transfer.units.items():
                    transferring[unit_type] += count

        return GroundUnitAllocations(
            self.base.armor,
            on_order,
            transferring,
        )

    @property
    def income_per_turn(self) -> int:
        return 0

    @property
    def has_active_frontline(self) -> bool:
        return any(not c.is_friendly(self.captured) for c in self.connected_points)

    def front_is_active(self, other: ControlPoint) -> bool:
        if other not in self.connected_points:
            raise ValueError

        return self.captured != other.captured

    @property
    def frontline_unit_count_limit(self) -> int:
        return (
            FREE_FRONTLINE_UNIT_SUPPLY
            + self.active_ammo_depots_count * AMMO_DEPOT_FRONTLINE_UNIT_CONTRIBUTION
        )

    @property
    def active_ammo_depots_count(self) -> int:
        """Return the number of available ammo depots"""
        return len(
            [
                obj
                for obj in self.connected_objectives
                if obj.category == "ammo" and not obj.is_dead
            ]
        )

    @property
    def total_ammo_depots_count(self) -> int:
        """Return the number of ammo depots, including dead ones"""
        return len([obj for obj in self.connected_objectives if obj.category == "ammo"])

    @property
    def strike_targets(self) -> List[Union[MissionTarget, Unit]]:
        return []

    @property
    @abstractmethod
    def category(self) -> str:
        ...

    @property
    @abstractmethod
    def status(self) -> ControlPointStatus:
        ...


class Airfield(ControlPoint):
    def __init__(
        self, airport: Airport, size: int, importance: float, has_frontline=True
    ):
        super().__init__(
            airport.id,
            airport.name,
            airport.position,
            airport,
            size,
            importance,
            has_frontline,
            cptype=ControlPointType.AIRBASE,
        )
        self.airport = airport
        self._runway_status = RunwayStatus()

    def can_operate(self, aircraft: FlyingType) -> bool:
        # TODO: Allow helicopters.
        # Need to implement ground spawns so the helos don't use the runway.
        # TODO: Allow harrier.
        # Needs ground spawns just like helos do, but also need to be able to
        # limit takeoff weight to ~20500 lbs or it won't be able to take off.
        return self.runway_is_operational()

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if not self.is_friendly(for_player):
            yield from [
                FlightType.OCA_AIRCRAFT,
                FlightType.OCA_RUNWAY,
            ]

        yield from super().mission_types(for_player)

        if self.is_friendly(for_player):
            yield from [
                FlightType.AEWC,
                # TODO: FlightType.INTERCEPTION
                # TODO: FlightType.LOGISTICS
            ]

    @property
    def total_aircraft_parking(self) -> int:
        return len(self.airport.parking_slots)

    @property
    def heading(self) -> int:
        return self.airport.runways[0].heading

    def runway_is_operational(self) -> bool:
        return not self.runway_status.damaged

    @property
    def runway_status(self) -> RunwayStatus:
        return self._runway_status

    def damage_runway(self) -> None:
        self.runway_status.damage()

    def active_runway(
        self, conditions: Conditions, dynamic_runways: Dict[str, RunwayData]
    ) -> RunwayData:
        assigner = RunwayAssigner(conditions)
        return assigner.get_preferred_runway(self.airport)

    @property
    def parking_slots(self) -> Iterator[ParkingSlot]:
        yield from self.airport.parking_slots

    @property
    def can_deploy_ground_units(self) -> bool:
        return True

    @property
    def income_per_turn(self) -> int:
        return 20

    @property
    def category(self) -> str:
        return "airfield"

    @property
    def status(self) -> ControlPointStatus:
        runway_staus = self.runway_status
        if runway_staus.needs_repair:
            return ControlPointStatus.Destroyed
        elif runway_staus.damaged:
            return ControlPointStatus.Damaged
        return ControlPointStatus.Functional


class NavalControlPoint(ControlPoint, ABC):
    @property
    def is_fleet(self) -> bool:
        return True

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if self.is_friendly(for_player):
            yield from [
                # TODO: FlightType.INTERCEPTION
                # TODO: Buddy tanking for the A-4?
                # TODO: Rescue chopper?
                # TODO: Inter-ship logistics?
            ]
        else:
            yield FlightType.ANTISHIP
        yield from super().mission_types(for_player)

    @property
    def heading(self) -> int:
        return 0  # TODO compute heading

    def find_main_tgo(self) -> TheaterGroundObject:
        for g in self.ground_objects:
            if g.dcs_identifier in ["CARRIER", "LHA"]:
                return g
        raise RuntimeError(f"Found no carrier/LHA group for {self.name}")

    def runway_is_operational(self) -> bool:
        # Necessary because it's possible for the carrier itself to have sunk
        # while its escorts are still alive.
        for group in self.find_main_tgo().groups:
            for u in group.units:
                if db.unit_type_from_name(u.type) in [
                    CVN_74_John_C__Stennis,
                    LHA_1_Tarawa,
                    CV_1143_5_Admiral_Kuznetsov,
                    Type_071_Amphibious_Transport_Dock,
                ]:
                    return True
        return False

    def active_runway(
        self, conditions: Conditions, dynamic_runways: Dict[str, RunwayData]
    ) -> RunwayData:
        # TODO: Assign TACAN and ICLS earlier so we don't need this.
        fallback = RunwayData(self.full_name, runway_heading=0, runway_name="")
        return dynamic_runways.get(self.name, fallback)

    @property
    def runway_status(self) -> RunwayStatus:
        return RunwayStatus(damaged=not self.runway_is_operational())

    @property
    def runway_can_be_repaired(self) -> bool:
        return False

    @property
    def moveable(self) -> bool:
        return True

    @property
    def can_deploy_ground_units(self) -> bool:
        return False

    @property
    def status(self) -> ControlPointStatus:
        if not self.runway_is_operational():
            return ControlPointStatus.Destroyed
        if self.find_main_tgo().dead_units:
            return ControlPointStatus.Damaged
        return ControlPointStatus.Functional


class Carrier(NavalControlPoint):
    def __init__(self, name: str, at: Point, cp_id: int):
        import game.theater.conflicttheater

        super().__init__(
            cp_id,
            name,
            at,
            at,
            game.theater.conflicttheater.SIZE_SMALL,
            1,
            has_frontline=False,
            cptype=ControlPointType.AIRCRAFT_CARRIER_GROUP,
        )

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        yield from super().mission_types(for_player)
        if self.is_friendly(for_player):
            yield FlightType.AEWC

    def capture(self, game: Game, for_player: bool) -> None:
        raise RuntimeError("Carriers cannot be captured")

    @property
    def is_carrier(self):
        return True

    def can_operate(self, aircraft: FlyingType) -> bool:
        return aircraft in db.CARRIER_CAPABLE

    @property
    def total_aircraft_parking(self) -> int:
        return 90

    @property
    def category(self) -> str:
        return "cv"


class Lha(NavalControlPoint):
    def __init__(self, name: str, at: Point, cp_id: int):
        import game.theater.conflicttheater

        super().__init__(
            cp_id,
            name,
            at,
            at,
            game.theater.conflicttheater.SIZE_SMALL,
            1,
            has_frontline=False,
            cptype=ControlPointType.LHA_GROUP,
        )

    def capture(self, game: Game, for_player: bool) -> None:
        raise RuntimeError("LHAs cannot be captured")

    @property
    def is_lha(self) -> bool:
        return True

    def can_operate(self, aircraft: FlyingType) -> bool:
        return aircraft in db.LHA_CAPABLE

    @property
    def total_aircraft_parking(self) -> int:
        return 20

    @property
    def category(self) -> str:
        return "lha"


class OffMapSpawn(ControlPoint):
    def runway_is_operational(self) -> bool:
        return True

    def __init__(self, cp_id: int, name: str, position: Point):
        from . import IMPORTANCE_MEDIUM, SIZE_REGULAR

        super().__init__(
            cp_id,
            name,
            position,
            at=position,
            size=SIZE_REGULAR,
            importance=IMPORTANCE_MEDIUM,
            has_frontline=False,
            cptype=ControlPointType.OFF_MAP,
        )

    def capture(self, game: Game, for_player: bool) -> None:
        raise RuntimeError("Off map control points cannot be captured")

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        yield from []

    @property
    def total_aircraft_parking(self) -> int:
        return 1000

    def can_operate(self, aircraft: FlyingType) -> bool:
        return True

    @property
    def heading(self) -> int:
        return 0

    def active_runway(
        self, conditions: Conditions, dynamic_runways: Dict[str, RunwayData]
    ) -> RunwayData:
        logging.warning("TODO: Off map spawns have no runways.")
        return RunwayData(self.full_name, runway_heading=0, runway_name="")

    @property
    def runway_status(self) -> RunwayStatus:
        return RunwayStatus()

    @property
    def can_deploy_ground_units(self) -> bool:
        return False

    @property
    def category(self) -> str:
        return "offmap"

    @property
    def status(self) -> ControlPointStatus:
        return ControlPointStatus.Functional


class Fob(ControlPoint):
    def __init__(self, name: str, at: Point, cp_id: int):
        import game.theater.conflicttheater

        super().__init__(
            cp_id,
            name,
            at,
            at,
            game.theater.conflicttheater.SIZE_SMALL,
            1,
            has_frontline=True,
            cptype=ControlPointType.FOB,
        )
        self.name = name

    def runway_is_operational(self) -> bool:
        return False

    def active_runway(
        self, conditions: Conditions, dynamic_runways: Dict[str, RunwayData]
    ) -> RunwayData:
        logging.warning("TODO: FOBs have no runways.")
        return RunwayData(self.full_name, runway_heading=0, runway_name="")

    @property
    def runway_status(self) -> RunwayStatus:
        return RunwayStatus()

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.STRIKE

        yield from super().mission_types(for_player)

    @property
    def total_aircraft_parking(self) -> int:
        return 0

    def can_operate(self, aircraft: FlyingType) -> bool:
        return False

    @property
    def heading(self) -> int:
        return 0

    @property
    def can_deploy_ground_units(self) -> bool:
        return True

    @property
    def income_per_turn(self) -> int:
        return 10

    @property
    def category(self) -> str:
        return "fob"

    @property
    def status(self) -> ControlPointStatus:
        return ControlPointStatus.Functional
