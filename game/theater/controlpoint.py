from __future__ import annotations

import heapq
import itertools
import logging
import math
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto, unique
from functools import cached_property, total_ordering
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    TYPE_CHECKING,
    Tuple,
    Type,
)
from uuid import UUID

from dcs.mapping import Point
from dcs.ships import (
    Ara_vdm,
    CVN_71,
    CVN_72,
    CVN_73,
    CVN_75,
    CV_1143_5,
    Forrestal,
    Hms_invincible,
    KUZNECOW,
    LHA_Tarawa,
    Stennis,
    Type_071,
)
from dcs.terrain.terrain import Airport, ParkingSlot
from dcs.unitgroup import ShipGroup, StaticGroup
from dcs.unittype import ShipType

from game.ato.closestairfields import ObjectiveDistanceCache
from game.ground_forces.combat_stance import CombatStance
from game.point_with_heading import PointWithHeading
from game.runways import RunwayAssigner, RunwayData
from game.scenery_group import SceneryGroup
from game.sidc import (
    Entity,
    LandInstallationEntity,
    SeaSurfaceEntity,
    SidcDescribable,
    StandardIdentity,
    Status,
    SymbolSet,
)
from game.theater.presetlocation import PresetLocation
from game.utils import Distance, Heading, meters
from .base import Base
from .frontline import FrontLine
from .missiontarget import MissionTarget
from .theatergroundobject import (
    GenericCarrierGroundObject,
    IadsGroundObject,
    TheaterGroundObject,
    VehicleGroupGroundObject,
)
from .theatergroup import TheaterUnit
from ..ato.starttype import StartType
from ..data.units import UnitClass
from ..db import Database
from ..dcs.aircrafttype import AircraftType
from ..dcs.groundunittype import GroundUnitType
from ..utils import nautical_miles
from ..weather.conditions import Conditions

if TYPE_CHECKING:
    from game import Game
    from game.ato.flighttype import FlightType
    from game.coalition import Coalition
    from game.lasercodes.lasercoderegistry import LaserCodeRegistry
    from game.sim import GameUpdateEvents
    from game.squadrons.squadron import Squadron
    from game.transfers import PendingTransfers
    from .conflicttheater import ConflictTheater

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
    ships: List[PresetLocation] = field(default_factory=list)

    #: Locations used by coastal defenses that are generated if the faction is capable.
    coastal_defenses: List[PresetLocation] = field(default_factory=list)

    #: Locations used by ground based strike objectives.
    strike_locations: List[PresetLocation] = field(default_factory=list)

    #: Locations used by offshore strike objectives.
    offshore_strike_locations: List[PresetLocation] = field(default_factory=list)

    #: Locations used by missile sites like scuds and V-2s that are generated if the
    #: faction is capable.
    missile_sites: List[PresetLocation] = field(default_factory=list)

    #: Locations of long range SAMs.
    long_range_sams: List[PresetLocation] = field(default_factory=list)

    #: Locations of medium range SAMs.
    medium_range_sams: List[PresetLocation] = field(default_factory=list)

    #: Locations of short range SAMs.
    short_range_sams: List[PresetLocation] = field(default_factory=list)

    #: Locations of AAA groups.
    aaa: List[PresetLocation] = field(default_factory=list)

    #: Locations of EWRs.
    ewrs: List[PresetLocation] = field(default_factory=list)

    #: Locations of map scenery to create zones for.
    scenery: List[SceneryGroup] = field(default_factory=list)

    #: Locations of factories for producing ground units.
    factories: List[PresetLocation] = field(default_factory=list)

    #: Locations of ammo depots for controlling number of units on the front line at a
    #: control point.
    ammunition_depots: List[PresetLocation] = field(default_factory=list)

    #: Locations of stationary armor groups.
    armor_groups: List[PresetLocation] = field(default_factory=list)

    #: Locations of skynet specific groups
    iads_connection_node: List[PresetLocation] = field(default_factory=list)
    iads_power_source: List[PresetLocation] = field(default_factory=list)
    iads_command_center: List[PresetLocation] = field(default_factory=list)


@dataclass(frozen=True)
class AircraftAllocations:
    present: dict[AircraftType, int]
    ordered: dict[AircraftType, int]
    transferring: dict[AircraftType, int]

    @property
    def total_value(self) -> int:
        total: int = 0
        for unit_type, count in self.present.items():
            total += unit_type.price * count
        for unit_type, count in self.ordered.items():
            total += unit_type.price * count
        for unit_type, count in self.transferring.items():
            total += unit_type.price * count

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
    present: dict[GroundUnitType, int]
    ordered: dict[GroundUnitType, int]
    transferring: dict[GroundUnitType, int]

    @property
    def all(self) -> dict[GroundUnitType, int]:
        combined: dict[GroundUnitType, int] = defaultdict(int)
        for unit_type, count in itertools.chain(
            self.present.items(), self.ordered.items(), self.transferring.items()
        ):
            combined[unit_type] += count
        return dict(combined)

    @property
    def total_value(self) -> int:
        total: int = 0
        for unit_type, count in self.present.items():
            total += unit_type.price * count
        for unit_type, count in self.ordered.items():
            total += unit_type.price * count
        for unit_type, count in self.transferring.items():
            total += unit_type.price * count

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

    def repair(self) -> None:
        self.repair_turns_remaining = None
        self.damaged = False

    def begin_repair(self) -> None:
        if self.repair_turns_remaining is not None:
            logging.error("Runway already under repair. Restarting.")
        self.repair_turns_remaining = 4

    def process_turn(self) -> None:
        if self.repair_turns_remaining is not None:
            if self.repair_turns_remaining == 1:
                self.repair()
            else:
                self.repair_turns_remaining -= 1

    @property
    def needs_repair(self) -> bool:
        return self.damaged and self.repair_turns_remaining is None

    def describe(self) -> str:
        if not self.damaged:
            return "operational"

        turns_remaining = self.repair_turns_remaining
        if turns_remaining is None:
            return "damaged"

        return f"repairing, {turns_remaining} turns remaining"


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


StartingPosition = ShipGroup | StaticGroup | Airport | Point


class ControlPoint(MissionTarget, SidcDescribable, ABC):
    # Not sure what distance DCS uses, but assuming it's about 2NM since that's roughly
    # the distance of the circle on the map.
    CAPTURE_DISTANCE = nautical_miles(2)

    # TODO: Only airbases have IDs.
    # TODO: cptype is obsolete.
    def __init__(
        self,
        name: str,
        position: Point,
        at: StartingPosition,
        theater: ConflictTheater,
        starts_blue: bool,
        cptype: ControlPointType = ControlPointType.AIRBASE,
    ) -> None:
        super().__init__(name, position)
        self.id = uuid.uuid4()
        self.full_name = name
        self.at = at
        self.theater = theater
        self.starts_blue = starts_blue
        self.connected_objectives: List[TheaterGroundObject] = []
        self.preset_locations = PresetLocations()
        self.helipads: List[PointWithHeading] = []

        self._coalition: Optional[Coalition] = None
        self.captured_invert = False
        self.front_lines: dict[ControlPoint, FrontLine] = {}
        # TODO: Should be Airbase specific.
        self.connected_points: List[ControlPoint] = []
        self.convoy_routes: Dict[ControlPoint, Tuple[Point, ...]] = {}
        self.shipping_lanes: Dict[ControlPoint, Tuple[Point, ...]] = {}
        self.base: Base = Base()
        self.cptype = cptype
        # TODO: Should be Airbase specific.
        self.stances: dict[UUID, CombatStance] = {}
        from ..groundunitorders import GroundUnitOrders

        self.ground_unit_orders = GroundUnitOrders(self)

        self.target_position: Optional[Point] = None
        self.ferry_only = False

        # Initialized late because ControlPoints are constructed before the game is.
        self._front_line_db: Database[FrontLine] | None = None

    def __repr__(self) -> str:
        return f"<{self.__class__}: {self.name}>"

    @property
    def dcs_airport(self) -> Airport | None:
        return None

    @property
    def coalition(self) -> Coalition:
        if self._coalition is None:
            raise RuntimeError("ControlPoint not fully initialized: coalition not set")
        return self._coalition

    def finish_init(self, game: Game) -> None:
        assert self._coalition is None
        self._coalition = game.coalition_for(self.starts_blue)
        assert self._front_line_db is None
        self._front_line_db = game.db.front_lines

    def initialize_turn_0(self, laser_code_registry: LaserCodeRegistry) -> None:
        # We don't need to send events for turn 0. The UI isn't up yet, and it'll fetch
        # the entire game state when it comes up.
        from game.sim import GameUpdateEvents

        self._create_missing_front_lines(laser_code_registry, GameUpdateEvents())

    @property
    def front_line_db(self) -> Database[FrontLine]:
        assert self._front_line_db is not None
        return self._front_line_db

    def _create_missing_front_lines(
        self, laser_code_registry: LaserCodeRegistry, events: GameUpdateEvents
    ) -> None:
        for connection in self.convoy_routes.keys():
            if not connection.front_line_active_with(
                self
            ) and not connection.is_friendly_to(self):
                self._create_front_line_with(laser_code_registry, connection, events)

    def _create_front_line_with(
        self,
        laser_code_registry: LaserCodeRegistry,
        connection: ControlPoint,
        events: GameUpdateEvents,
    ) -> None:
        blue, red = FrontLine.sort_control_points(self, connection)
        front = FrontLine(blue, red, laser_code_registry.alloc_laser_code())
        self.front_lines[connection] = front
        connection.front_lines[self] = front
        self.front_line_db.add(front.id, front)
        events.update_front_line(front)

    def _remove_front_line_with(
        self,
        connection: ControlPoint,
        events: GameUpdateEvents,
    ) -> None:
        front = self.front_lines[connection]
        del self.front_lines[connection]
        del connection.front_lines[self]
        self.front_line_db.remove(front.id)
        front.laser_code.release()
        events.delete_front_line(front)

    def _clear_front_lines(self, events: GameUpdateEvents) -> None:
        for opponent in list(self.front_lines.keys()):
            self._remove_front_line_with(opponent, events)

    @property
    def has_frontline(self) -> bool:
        return bool(self.front_lines)

    def front_line_active_with(self, other: ControlPoint) -> bool:
        return other in self.front_lines

    def front_line_with(self, other: ControlPoint) -> FrontLine:
        return self.front_lines[other]

    @property
    def captured(self) -> bool:
        return self.coalition.player

    @property
    def standard_identity(self) -> StandardIdentity:
        return (
            StandardIdentity.FRIEND if self.captured else StandardIdentity.HOSTILE_FAKER
        )

    @property
    def sidc_status(self) -> Status:
        if self.status is ControlPointStatus.Functional:
            return Status.PRESENT
        if self.status is ControlPointStatus.Damaged:
            return Status.PRESENT_DAMAGED
        if self.status is ControlPointStatus.Destroyed:
            return Status.PRESENT_DESTROYED
        raise ValueError(f"Unexpected ControlPointStatus: {self.status}")

    @property
    def ground_objects(self) -> List[TheaterGroundObject]:
        return list(self.connected_objectives)

    @property
    def squadrons(self) -> Iterator[Squadron]:
        for squadron in self.coalition.air_wing.iter_squadrons():
            if squadron.location == self:
                yield squadron

    @property
    @abstractmethod
    def heading(self) -> Heading:
        ...

    def __str__(self) -> str:
        return self.name

    @property
    def is_isolated(self) -> bool:
        return not self.connected_points

    @property
    def is_global(self) -> bool:
        return self.is_isolated

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

    @property
    def has_helipads(self) -> bool:
        """
        Returns true if cp has helipads
        """
        return len(self.helipads) > 0

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
    def is_carrier(self) -> bool:
        """
        :return: Whether this control point is an aircraft carrier
        """
        return False

    @property
    def is_fleet(self) -> bool:
        """
        :return: Whether this control point is a boat (mobile)
        """
        return False

    @property
    def is_lha(self) -> bool:
        """
        :return: Whether this control point is an LHA
        """
        return False

    @property
    def moveable(self) -> bool:
        """
        :return: Whether this control point can be moved around
        """
        return self.max_move_distance > meters(0)

    @property
    def max_move_distance(self) -> Distance:
        return meters(0)

    def destination_in_range(self, destination: Point) -> bool:
        distance = meters(destination.distance_to_point(self.position))
        return distance <= self.max_move_distance

    @property
    @abstractmethod
    def can_deploy_ground_units(self) -> bool:
        ...

    @property
    @abstractmethod
    def total_aircraft_parking(self) -> int:
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
    def get_carrier_group_name(self) -> Optional[str]:
        """
        Get the carrier group name if the airbase is a carrier
        :return: Carrier group name
        """
        if self.cptype in [
            ControlPointType.AIRCRAFT_CARRIER_GROUP,
            ControlPointType.LHA_GROUP,
        ]:
            for g in self.ground_objects:
                for group in g.groups:
                    for u in group.units:
                        if u.unit_type and u.unit_type.unit_class in [
                            UnitClass.AIRCRAFT_CARRIER,
                            UnitClass.HELICOPTER_CARRIER,
                        ]:
                            return group.group_name
        return None

    def get_carrier_group_type(
        self, always_supercarrier: bool = False
    ) -> Optional[Type[ShipType]]:
        """
        Get the carrier group type if the airbase is a carrier. Arguments:
            always_supercarrier: True if should always return the supercarrier type, False if should only
                return the supercarrier type when the supercarrier option is enabled in settings.
        :return: Carrier group type
        """
        if self.cptype in [
            ControlPointType.AIRCRAFT_CARRIER_GROUP,
            ControlPointType.LHA_GROUP,
        ]:
            for g in self.ground_objects:
                for group in g.groups:
                    u = group.units[0]
                    carrier_type = u.type
                    if (
                        u.unit_type
                        and u.unit_type.unit_class
                        in [
                            UnitClass.AIRCRAFT_CARRIER,
                            UnitClass.HELICOPTER_CARRIER,
                        ]
                        and issubclass(carrier_type, ShipType)
                    ):
                        if (
                            self.coalition.game.settings.supercarrier
                            or always_supercarrier
                        ):
                            return self.upgrade_to_supercarrier(carrier_type, self.name)
                        return carrier_type
        return None

    @staticmethod
    def upgrade_to_supercarrier(unit: Type[ShipType], name: str) -> Type[ShipType]:
        if unit == Stennis:
            if name == "CVN-71 Theodore Roosevelt":
                return CVN_71
            elif name == "CVN-72 Abraham Lincoln":
                return CVN_72
            elif name == "CVN-73 George Washington":
                return CVN_73
            elif name == "CVN-75 Harry S. Truman":
                return CVN_75
            elif name == "Carrier Strike Group 8":
                return CVN_75
            else:
                return CVN_71
        elif unit == KUZNECOW:
            return CV_1143_5
        else:
            return unit

    # TODO: Should be Airbase specific.
    def is_connected(self, to: ControlPoint) -> bool:
        return to in self.connected_points

    def find_ground_objects_by_obj_name(
        self, obj_name: str
    ) -> list[TheaterGroundObject]:
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

    def retreat_ground_units(self, game: Game) -> None:
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

    def capture_aircraft(self, game: Game, airframe: AircraftType, count: int) -> None:
        value = airframe.price * count
        game.adjust_budget(value, player=not self.captured)
        game.message(
            f"No valid retreat destination in range of {self.name} for {airframe} "
            f"{count} aircraft have been captured and sold for ${value}M."
        )

    def aircraft_retreat_destination(
        self, squadron: Squadron
    ) -> Optional[ControlPoint]:
        closest = ObjectiveDistanceCache.get_closest_airfields(self)
        max_retreat_distance = squadron.aircraft.max_mission_range
        # Skip the first airbase because that's the airbase we're retreating
        # from.
        airfields = list(closest.operational_airfields_within(max_retreat_distance))[1:]
        not_preferred: Optional[ControlPoint] = None
        overfull: list[ControlPoint] = []
        for airbase in airfields:
            if airbase.captured != self.captured:
                continue

            if airbase.unclaimed_parking() < squadron.owned_aircraft:
                if airbase.can_operate(squadron.aircraft):
                    overfull.append(airbase)
                continue

            if squadron.operates_from(airbase):
                # Has room, is a preferred base type for this squadron, and is the
                # closest choice. No need to keep looking.
                return airbase

            if not_preferred is None and airbase.can_operate(squadron.aircraft):
                # Has room and is capable of operating from this base, but it isn't
                # preferred. Remember this option and use it if we can't find a
                # preferred base type with room.
                not_preferred = airbase
        if not_preferred is not None:
            # It's not our best choice but the other choices don't have room for the
            # squadron and would lead to aircraft being captured.
            return not_preferred

        # No base was available with enough room. Find whichever base has the most room
        # available so we lose as little as possible. The overfull list is already
        # sorted by distance, and filtered for appropriate destinations.
        base_for_fewest_losses: Optional[ControlPoint] = None
        loss_count = math.inf
        for airbase in overfull:
            overflow = -(
                airbase.unclaimed_parking()
                - squadron.owned_aircraft
                - squadron.pending_deliveries
            )
            if overflow < loss_count:
                loss_count = overflow
                base_for_fewest_losses = airbase
        return base_for_fewest_losses

    def _retreat_squadron(self, game: Game, squadron: Squadron) -> None:
        destination = self.aircraft_retreat_destination(squadron)
        if destination is None:
            squadron.refund_orders()
            self.capture_aircraft(game, squadron.aircraft, squadron.owned_aircraft)
            return
        logging.debug(f"{squadron} retreating to {destination} from {self}")
        squadron.relocate_to(destination)
        squadron.cancel_overflow_orders()
        overflow = -destination.unclaimed_parking()
        if overflow > 0:
            logging.debug(
                f"Not enough room for {squadron} at {destination}. Capturing "
                f"{overflow} aircraft."
            )
            self.capture_aircraft(game, squadron.aircraft, overflow)
            squadron.owned_aircraft -= overflow

    def retreat_air_units(self, game: Game) -> None:
        # TODO: Capture in order of price to retain maximum value?
        for squadron in self.squadrons:
            self._retreat_squadron(game, squadron)

    def depopulate_uncapturable_tgos(self) -> None:
        # TODO Rework this.
        for tgo in self.connected_objectives:
            if not tgo.capturable:
                tgo.clear()

    # TODO: Should be Airbase specific.
    def capture(self, game: Game, events: GameUpdateEvents, for_player: bool) -> None:
        new_coalition = game.coalition_for(for_player)
        self.ground_unit_orders.refund_all(self.coalition)
        self.retreat_ground_units(game)
        self.retreat_air_units(game)
        self.depopulate_uncapturable_tgos()
        self._coalition = new_coalition
        self.base.set_strength_to_minimum()
        self._clear_front_lines(events)
        self._create_missing_front_lines(game.laser_code_registry, events)
        events.update_control_point(self)

        # All the attached TGOs have either been depopulated or captured. Tell the UI to
        # update their state. Also update the orientation of all TGOs
        iads_update_required = False
        iads_network = game.theater.iads_network
        for tgo in self.connected_objectives:
            if isinstance(tgo, IadsGroundObject) or isinstance(
                tgo, VehicleGroupGroundObject
            ):
                if not iads_update_required and tgo in iads_network.participating:
                    iads_update_required = True
                conflict_heading = game.theater.heading_to_conflict_from(tgo.position)
                tgo.rotate(conflict_heading or tgo.heading)
            if not tgo.is_control_point:
                events.update_tgo(tgo)

        # Update the IADS Network
        if iads_update_required:
            iads_network.update_network(events)

    @property
    def required_aircraft_start_type(self) -> Optional[StartType]:
        return None

    @abstractmethod
    def can_operate(self, aircraft: AircraftType) -> bool:
        ...

    def unclaimed_parking(self) -> int:
        return self.total_aircraft_parking - self.allocated_aircraft().total

    @abstractmethod
    def active_runway(
        self,
        theater: ConflictTheater,
        conditions: Conditions,
        dynamic_runways: Dict[str, RunwayData],
    ) -> RunwayData:
        ...

    def stub_runway_data(self) -> RunwayData:
        return RunwayData(
            self.full_name, runway_heading=Heading.from_degrees(0), runway_name=""
        )

    @property
    def airdrome_id_for_landing(self) -> Optional[int]:
        return None

    @property
    def parking_slots(self) -> Iterator[ParkingSlot]:
        yield from []

    @property
    @abstractmethod
    def runway_is_destroyable(self) -> bool:
        ...

    @property
    @abstractmethod
    def runway_status(self) -> RunwayStatus:
        ...

    @abstractmethod
    def describe_runway_status(self) -> str | None:
        """Description of the runway status suitable for UI use."""

    @property
    def runway_can_be_repaired(self) -> bool:
        return self.runway_status.needs_repair

    def begin_runway_repair(self) -> None:
        if not self.runway_can_be_repaired:
            logging.error(f"Cannot repair runway at {self}")
            return
        self.runway_status.begin_repair()

    def process_turn(self, game: Game) -> None:
        # We're running at the end of the turn, so the time right now is irrelevant, and
        # we don't know what time the next turn will start yet. It doesn't actually
        # matter though, because the first thing the start of turn action will do is
        # clear the ATO and replan the airlifts with the correct time.
        self.ground_unit_orders.process(game, game.conditions.start_time)

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

    def allocated_aircraft(self) -> AircraftAllocations:
        present: dict[AircraftType, int] = defaultdict(int)
        on_order: dict[AircraftType, int] = defaultdict(int)
        transferring: dict[AircraftType, int] = defaultdict(int)
        for squadron in self.squadrons:
            present[squadron.aircraft] += squadron.owned_aircraft
            if squadron.destination is None:
                on_order[squadron.aircraft] += squadron.pending_deliveries
            else:
                transferring[squadron.aircraft] -= squadron.owned_aircraft
        for squadron in self.coalition.air_wing.iter_squadrons():
            if squadron.destination == self:
                on_order[squadron.aircraft] += squadron.pending_deliveries
                transferring[squadron.aircraft] += squadron.owned_aircraft

        return AircraftAllocations(present, on_order, transferring)

    def allocated_ground_units(
        self, transfers: PendingTransfers
    ) -> GroundUnitAllocations:
        on_order = {}
        for unit_bought, count in self.ground_unit_orders.units.items():
            if isinstance(unit_bought, GroundUnitType):
                on_order[unit_bought] = count

        transferring: dict[GroundUnitType, int] = defaultdict(int)
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
    def deployable_front_line_units(self) -> int:
        return self.deployable_front_line_units_with(self.active_ammo_depots_count)

    def deployable_front_line_units_with(self, ammo_depot_count: int) -> int:
        return min(
            self.front_line_capacity_with(ammo_depot_count), self.base.total_armor
        )

    @classmethod
    def front_line_capacity_with(cls, ammo_depot_count: int) -> int:
        return (
            FREE_FRONTLINE_UNIT_SUPPLY
            + ammo_depot_count * AMMO_DEPOT_FRONTLINE_UNIT_CONTRIBUTION
        )

    @property
    def frontline_unit_count_limit(self) -> int:
        return self.front_line_capacity_with(self.active_ammo_depots_count)

    @property
    def all_ammo_depots(self) -> Iterator[TheaterGroundObject]:
        for tgo in self.connected_objectives:
            if tgo.is_ammo_depot:
                yield tgo

    def ammo_depot_count(self, alive_only: bool = False) -> int:
        return sum(
            ammo_depot.alive_unit_count if alive_only else ammo_depot.unit_count
            for ammo_depot in self.all_ammo_depots
        )

    @property
    def active_ammo_depots_count(self) -> int:
        """Return the number of available ammo depots"""
        return self.ammo_depot_count(True)

    @property
    def total_ammo_depots_count(self) -> int:
        """Return the number of ammo depots, including dead ones"""
        return self.ammo_depot_count()

    @property
    def active_fuel_depots_count(self) -> int:
        """Return the number of available fuel depots"""
        return len(
            [
                obj
                for obj in self.connected_objectives
                if obj.category == "fuel" and not obj.is_dead
            ]
        )

    @property
    def total_fuel_depots_count(self) -> int:
        """Return the number of fuel depots, including dead ones"""
        return len([obj for obj in self.connected_objectives if obj.category == "fuel"])

    @property
    def strike_targets(self) -> list[TheaterUnit]:
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
        self, airport: Airport, theater: ConflictTheater, starts_blue: bool
    ) -> None:
        super().__init__(
            airport.name,
            airport.position,
            airport,
            theater,
            starts_blue,
            cptype=ControlPointType.AIRBASE,
        )
        self.airport = airport
        self._runway_status = RunwayStatus()

    @property
    def dcs_airport(self) -> Airport:
        return self.airport

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_INSTALLATIONS, LandInstallationEntity.AIPORT_AIR_BASE

    def can_operate(self, aircraft: AircraftType) -> bool:
        # TODO: Allow helicopters.
        # Need to implement ground spawns so the helos don't use the runway.
        # TODO: Allow harrier.
        # Needs ground spawns just like helos do, but also need to be able to
        # limit takeoff weight to ~20500 lbs or it won't be able to take off.

        # return false if aircraft is fixed wing and airport has no runways
        if not aircraft.helicopter and not self.airport.runways:
            return False
        else:
            return self.runway_is_operational()

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield from [
                FlightType.OCA_AIRCRAFT,
                FlightType.OCA_RUNWAY,
                FlightType.AIR_ASSAULT,
            ]

        yield from super().mission_types(for_player)

        if self.is_friendly(for_player):
            yield from [
                FlightType.AEWC,
                # TODO: FlightType.INTERCEPTION
                # TODO: FlightType.LOGISTICS
            ]

        yield FlightType.REFUELING

    @property
    def total_aircraft_parking(self) -> int:
        """
        Return total aircraft parking slots available
        Note : additional helipads shouldn't contribute to this score as it could allow airfield
        to buy more planes than what they are able to host
        """
        return len(self.airport.parking_slots)

    @property
    def heading(self) -> Heading:
        return Heading.from_degrees(self.airport.runways[0].heading)

    @property
    def runway_is_destroyable(self) -> bool:
        return True

    def runway_is_operational(self) -> bool:
        return not self.runway_status.damaged

    @property
    def runway_status(self) -> RunwayStatus:
        return self._runway_status

    def describe_runway_status(self) -> str:
        return f"Runway {self.runway_status.describe()}"

    def damage_runway(self) -> None:
        self.runway_status.damage()

    def active_runway(
        self,
        theater: ConflictTheater,
        conditions: Conditions,
        dynamic_runways: Dict[str, RunwayData],
    ) -> RunwayData:
        if not self.airport.runways:
            # Some airfields are heliports and don't have any runways. This isn't really
            # the best fix, since we should still try to generate partial data for TACAN
            # beacons, but it'll do for a bug fix, and the proper fix probably involves
            # making heliports their own CP type.
            # https://github.com/dcs-liberation/dcs_liberation/issues/2710
            return self.stub_runway_data()

        assigner = RunwayAssigner(conditions)
        return assigner.get_preferred_runway(theater, self.airport)

    @property
    def airdrome_id_for_landing(self) -> Optional[int]:
        return self.airport.id

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
        from game.ato import FlightType

        if self.is_friendly(for_player):
            yield from [
                FlightType.AEWC,
                FlightType.REFUELING,
                # TODO: FlightType.INTERCEPTION
                # TODO: Buddy tanking for the A-4?
                # TODO: Rescue chopper?
                # TODO: Inter-ship logistics?
            ]
        else:
            yield FlightType.ANTISHIP
        yield from super().mission_types(for_player)

    @property
    def heading(self) -> Heading:
        return Heading.from_degrees(0)  # TODO compute heading

    def find_main_tgo(self) -> GenericCarrierGroundObject:
        for g in self.ground_objects:
            if isinstance(g, GenericCarrierGroundObject):
                return g
        raise RuntimeError(f"Found no carrier/LHA group for {self.name}")

    @property
    def runway_is_destroyable(self) -> bool:
        return False

    def runway_is_operational(self) -> bool:
        # Necessary because it's possible for the carrier itself to have sunk
        # while its escorts are still alive.
        for group in self.find_main_tgo().groups:
            for u in group.units:
                if u.alive and u.type in [
                    Ara_vdm,
                    Forrestal,
                    Hms_invincible,
                    KUZNECOW,
                    LHA_Tarawa,
                    Stennis,
                    Type_071,
                ]:
                    return True
        return False

    def active_runway(
        self,
        theater: ConflictTheater,
        conditions: Conditions,
        dynamic_runways: Dict[str, RunwayData],
    ) -> RunwayData:
        # TODO: Assign TACAN and ICLS earlier so we don't need this.
        fallback = RunwayData(
            self.full_name, runway_heading=Heading.from_degrees(0), runway_name=""
        )
        return dynamic_runways.get(self.name, fallback)

    @property
    def runway_status(self) -> RunwayStatus:
        return RunwayStatus(damaged=not self.runway_is_operational())

    def describe_runway_status(self) -> str:
        return f"Flight deck {self.runway_status.describe()}"

    @property
    def runway_can_be_repaired(self) -> bool:
        return False

    @property
    def max_move_distance(self) -> Distance:
        return nautical_miles(80)

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
    def __init__(
        self, name: str, at: Point, theater: ConflictTheater, starts_blue: bool
    ):
        super().__init__(
            name,
            at,
            at,
            theater,
            starts_blue,
            cptype=ControlPointType.AIRCRAFT_CARRIER_GROUP,
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.CARRIER

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        yield from super().mission_types(for_player)
        if self.is_friendly(for_player):
            yield from [
                # Nothing yet.
            ]

    def capture(self, game: Game, events: GameUpdateEvents, for_player: bool) -> None:
        raise RuntimeError("Carriers cannot be captured")

    @property
    def is_carrier(self) -> bool:
        return True

    def can_operate(self, aircraft: AircraftType) -> bool:
        return aircraft.carrier_capable

    @property
    def total_aircraft_parking(self) -> int:
        return 90

    @property
    def category(self) -> str:
        return "cv"


class Lha(NavalControlPoint):
    def __init__(
        self, name: str, at: Point, theater: ConflictTheater, starts_blue: bool
    ):
        super().__init__(
            name, at, at, theater, starts_blue, cptype=ControlPointType.LHA_GROUP
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.SEA_SURFACE, SeaSurfaceEntity.AMPHIBIOUS_ASSAULT_SHIP_GENERAL

    def capture(self, game: Game, events: GameUpdateEvents, for_player: bool) -> None:
        raise RuntimeError("LHAs cannot be captured")

    @property
    def is_lha(self) -> bool:
        return True

    def can_operate(self, aircraft: AircraftType) -> bool:
        return aircraft.lha_capable

    @property
    def total_aircraft_parking(self) -> int:
        return 20

    @property
    def category(self) -> str:
        return "lha"


class OffMapSpawn(ControlPoint):
    def runway_is_operational(self) -> bool:
        return True

    def __init__(
        self, name: str, position: Point, theater: ConflictTheater, starts_blue: bool
    ):
        super().__init__(
            name,
            position,
            position,
            theater,
            starts_blue,
            cptype=ControlPointType.OFF_MAP,
        )

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_INSTALLATIONS, LandInstallationEntity.AIPORT_AIR_BASE

    def capture(self, game: Game, events: GameUpdateEvents, for_player: bool) -> None:
        raise RuntimeError("Off map control points cannot be captured")

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        yield from []

    @property
    def total_aircraft_parking(self) -> int:
        return 1000

    def can_operate(self, aircraft: AircraftType) -> bool:
        return True

    @property
    def required_aircraft_start_type(self) -> Optional[StartType]:
        return StartType.IN_FLIGHT

    @property
    def heading(self) -> Heading:
        return Heading.from_degrees(0)

    def active_runway(
        self,
        theater: ConflictTheater,
        conditions: Conditions,
        dynamic_runways: Dict[str, RunwayData],
    ) -> RunwayData:
        logging.warning("TODO: Off map spawns have no runways.")
        return self.stub_runway_data()

    @property
    def runway_is_destroyable(self) -> bool:
        return False

    @property
    def runway_status(self) -> RunwayStatus:
        return RunwayStatus()

    def describe_runway_status(self) -> str:
        return f"Off-map airport {self.runway_status.describe()}"

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
    def __init__(
        self, name: str, at: Point, theater: ConflictTheater, starts_blue: bool
    ):
        super().__init__(
            name, at, at, theater, starts_blue, cptype=ControlPointType.FOB
        )
        self.name = name

    @property
    def symbol_set_and_entity(self) -> tuple[SymbolSet, Entity]:
        return SymbolSet.LAND_INSTALLATIONS, LandInstallationEntity.MILITARY_BASE

    @property
    def runway_is_destroyable(self) -> bool:
        return False

    def runway_is_operational(self) -> bool:
        return self.has_helipads

    def active_runway(
        self,
        theater: ConflictTheater,
        conditions: Conditions,
        dynamic_runways: Dict[str, RunwayData],
    ) -> RunwayData:
        logging.warning("TODO: FOBs have no runways.")
        return self.stub_runway_data()

    @property
    def runway_status(self) -> RunwayStatus:
        return RunwayStatus()

    def describe_runway_status(self) -> str | None:
        if not self.has_helipads:
            return None
        return f"FARP {self.runway_status.describe()}"

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if not self.is_friendly(for_player):
            yield FlightType.STRIKE
            yield FlightType.AIR_ASSAULT
        else:
            yield FlightType.AEWC

        yield from super().mission_types(for_player)

    @property
    def total_aircraft_parking(self) -> int:
        return len(self.helipads)

    def can_operate(self, aircraft: AircraftType) -> bool:
        # FOBs and FARPs are the same class, distinguished only by non-FARP FOBs having
        # zero parking.
        # https://github.com/dcs-liberation/dcs_liberation/issues/2378
        return aircraft.helicopter and self.total_aircraft_parking > 0

    @property
    def heading(self) -> Heading:
        return Heading.from_degrees(0)

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
