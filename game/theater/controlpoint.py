from __future__ import annotations

import heapq
import itertools
import logging
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering
from typing import Any, Dict, Iterator, List, Optional, TYPE_CHECKING, Type

from dcs.mapping import Point
from dcs.ships import (
    CVN_74_John_C__Stennis,
    CV_1143_5_Admiral_Kuznetsov,
    LHA_1_Tarawa,
    Type_071_Amphibious_Transport_Dock,
)
from dcs.terrain.terrain import Airport, ParkingSlot
from dcs.unittype import FlyingType

from game import db
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.ground_forces.ai_ground_planner_db import TYPE_SHORAD
from gen.ground_forces.combat_stance import CombatStance
from gen.runways import RunwayAssigner, RunwayData
from .base import Base
from .missiontarget import MissionTarget
from game.point_with_heading import PointWithHeading
from .theatergroundobject import (
    BaseDefenseGroundObject,
    EwrGroundObject,
    GenericCarrierGroundObject,
    SamGroundObject,
    TheaterGroundObject,
    VehicleGroupGroundObject,
)
from ..db import PRICES
from ..utils import nautical_miles
from ..weather import Conditions

if TYPE_CHECKING:
    from game import Game
    from gen.flights.flight import FlightType


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


class LocationType(Enum):
    BaseAirDefense = "base air defense"
    Coastal = "coastal defense"
    Ewr = "EWR"
    Garrison = "garrison"
    MissileSite = "missile site"
    OffshoreStrikeTarget = "offshore strike target"
    Sam = "SAM"
    Ship = "ship"
    Shorad = "SHORAD"
    StrikeTarget = "strike target"


@dataclass
class PresetLocations:
    """Defines the preset locations loaded from the campaign mission file."""

    #: Locations used for spawning ground defenses for bases.
    base_garrisons: List[PointWithHeading] = field(default_factory=list)

    #: Locations used for spawning air defenses for bases. Used by SAMs, AAA,
    #: and SHORADs.
    base_air_defense: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by EWRs.
    ewrs: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by non-carrier ships. Carriers and LHAs are not random.
    ships: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by coastal defenses.
    coastal_defenses: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by ground based strike objectives.
    strike_locations: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by offshore strike objectives.
    offshore_strike_locations: List[PointWithHeading] = field(default_factory=list)

    #: Locations used by missile sites like scuds and V-2s.
    missile_sites: List[PointWithHeading] = field(default_factory=list)

    #: Locations of long range SAMs which should always be spawned.
    required_long_range_sams: List[PointWithHeading] = field(default_factory=list)

    #: Locations of medium range SAMs which should always be spawned.
    required_medium_range_sams: List[PointWithHeading] = field(default_factory=list)

    @staticmethod
    def _random_from(points: List[PointWithHeading]) -> Optional[PointWithHeading]:
        """Finds, removes, and returns a random position from the given list."""
        if not points:
            return None
        point = random.choice(points)
        points.remove(point)
        return point

    def random_for(self, location_type: LocationType) -> Optional[PointWithHeading]:
        """Returns a position suitable for the given location type.

        The location, if found, will be claimed by the caller and not available
        to subsequent calls.
        """
        if location_type == LocationType.BaseAirDefense:
            return self._random_from(self.base_air_defense)
        if location_type == LocationType.Coastal:
            return self._random_from(self.coastal_defenses)
        if location_type == LocationType.Ewr:
            return self._random_from(self.ewrs)
        if location_type == LocationType.Garrison:
            return self._random_from(self.base_garrisons)
        if location_type == LocationType.MissileSite:
            return self._random_from(self.missile_sites)
        if location_type == LocationType.OffshoreStrikeTarget:
            return self._random_from(self.offshore_strike_locations)
        if location_type == LocationType.Sam:
            return self._random_from(self.strike_locations)
        if location_type == LocationType.Ship:
            return self._random_from(self.ships)
        if location_type == LocationType.Shorad:
            return self._random_from(self.base_garrisons)
        if location_type == LocationType.StrikeTarget:
            return self._random_from(self.strike_locations)
        logging.error(f"Unknown location type: {location_type}")
        return None


@dataclass(frozen=True)
class PendingOccupancy:
    present: int
    ordered: int
    transferring: int

    @property
    def total(self) -> int:
        return self.present + self.ordered + self.transferring


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
        self.base_defenses: List[BaseDefenseGroundObject] = []
        self.preset_locations = PresetLocations()

        # TODO: Should be Airbase specific.
        self.size = size
        self.importance = importance
        self.captured = False
        self.captured_invert = False
        # TODO: Should be Airbase specific.
        self.has_frontline = has_frontline
        self.connected_points: List[ControlPoint] = []
        self.base: Base = Base()
        self.cptype = cptype
        # TODO: Should be Airbase specific.
        self.stances: Dict[int, CombatStance] = {}
        from ..event import UnitsDeliveryEvent

        self.pending_unit_deliveries = UnitsDeliveryEvent(self)

        self.target_position: Optional[Point] = None

    def __repr__(self):
        return f"<{__class__}: {self.name}>"

    @property
    def ground_objects(self) -> List[TheaterGroundObject]:
        return list(itertools.chain(self.connected_objectives, self.base_defenses))

    @property
    @abstractmethod
    def heading(self) -> int:
        ...

    def __str__(self):
        return self.name

    @property
    def is_global(self):
        return not self.connected_points

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

    # TODO: Should be Airbase specific.
    def connect(self, to: ControlPoint) -> None:
        self.connected_points.append(to)
        self.stances[to.id] = CombatStance.DEFENSIVE

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

    # TODO: Should be Airbase specific.
    def clear_base_defenses(self) -> None:
        for base_defense in self.base_defenses:
            p = PointWithHeading.from_point(base_defense.position, base_defense.heading)
            if isinstance(base_defense, EwrGroundObject):
                self.preset_locations.ewrs.append(p)
            elif isinstance(base_defense, SamGroundObject):
                self.preset_locations.base_air_defense.append(p)
            elif isinstance(base_defense, VehicleGroupGroundObject):
                self.preset_locations.base_garrisons.append(p)
            else:
                logging.error(
                    "Could not determine preset location type for "
                    f"{base_defense}. Assuming garrison type."
                )
                self.preset_locations.base_garrisons.append(p)
        self.base_defenses = []

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
                destination.control_point.base.commision_units({unit_type: 1})
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
        airfields = list(closest.airfields_within(max_retreat_distance))[1:]
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
            destination.base.commision_units({airframe: transfer_amount})
            count -= transfer_amount

    def retreat_air_units(self, game: Game) -> None:
        # TODO: Capture in order of price to retain maximum value?
        while self.base.aircraft:
            airframe, count = self.base.aircraft.popitem()
            self._retreat_air_units(game, airframe, count)

    # TODO: Should be Airbase specific.
    def capture(self, game: Game, for_player: bool) -> None:
        self.pending_unit_deliveries.refund_all(game)
        self.retreat_ground_units(game)
        self.retreat_air_units(game)

        if for_player:
            self.captured = True
        else:
            self.captured = False

        self.base.set_strength_to_minimum()

        self.clear_base_defenses()
        from .start_generator import BaseDefenseGenerator

        BaseDefenseGenerator(game, self).generate()

    @abstractmethod
    def can_operate(self, aircraft: Type[FlyingType]) -> bool:
        ...

    def aircraft_transferring(self, game: Game) -> int:
        if self.captured:
            ato = game.blue_ato
        else:
            ato = game.red_ato

        total = 0
        for package in ato.packages:
            for flight in package.flights:
                if flight.departure == flight.arrival:
                    continue
                if flight.departure == self:
                    total -= flight.count
                elif flight.arrival == self:
                    total += flight.count
        return total

    def expected_aircraft_next_turn(self, game: Game) -> PendingOccupancy:
        on_order = 0
        for unit_bought in self.pending_unit_deliveries.units:
            if issubclass(unit_bought, FlyingType):
                on_order += self.pending_unit_deliveries.units[unit_bought]

        return PendingOccupancy(
            self.base.total_aircraft, on_order, self.aircraft_transferring(game)
        )

    def unclaimed_parking(self, game: Game) -> int:
        return (
            self.total_aircraft_parking - self.expected_aircraft_next_turn(game).total
        )

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

    @property
    def pending_frontline_aa_deliveries_count(self):
        """
        Get number of pending frontline aa units
        """
        if self.pending_unit_deliveries:
            return sum(
                [
                    v
                    for k, v in self.pending_unit_deliveries.units.items()
                    if k in TYPE_SHORAD
                ]
            )
        else:
            return 0

    @property
    def pending_deliveries_count(self):
        """
        Get number of pending units
        """
        if self.pending_unit_deliveries:
            return sum([v for k, v in self.pending_unit_deliveries.units.items()])
        else:
            return 0

    @property
    def expected_ground_units_next_turn(self) -> PendingOccupancy:
        on_order = 0
        for unit_bought in self.pending_unit_deliveries.units:
            if issubclass(unit_bought, FlyingType):
                continue
            if unit_bought in TYPE_SHORAD:
                continue
            on_order += self.pending_unit_deliveries.units[unit_bought]

        return PendingOccupancy(
            self.base.total_armor,
            on_order,
            # Ground unit transfers not yet implemented.
            transferring=0,
        )

    @property
    def income_per_turn(self) -> int:
        return 0

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType

        if self.is_friendly(for_player):
            yield from [
                FlightType.AEWC,
            ]
        yield from super().mission_types(for_player)

    @property
    def has_active_frontline(self) -> bool:
        return any(not c.is_friendly(self.captured) for c in self.connected_points)


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

        if self.is_friendly(for_player):
            yield from [
                # TODO: FlightType.INTERCEPTION
                # TODO: FlightType.LOGISTICS
            ]
        else:
            yield from [
                FlightType.OCA_AIRCRAFT,
                FlightType.OCA_RUNWAY,
            ]
        yield from super().mission_types(for_player)

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

    def runway_is_operational(self) -> bool:
        # Necessary because it's possible for the carrier itself to have sunk
        # while its escorts are still alive.
        for g in self.ground_objects:
            if g.dcs_identifier in ["CARRIER", "LHA"]:
                for group in g.groups:
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

        if self.is_friendly(for_player):
            yield from [
                FlightType.BARCAP,
                # TODO: FlightType.LOGISTICS
            ]
        else:
            yield from [
                FlightType.STRIKE,
                FlightType.SWEEP,
                FlightType.ESCORT,
                FlightType.SEAD,
            ]

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
