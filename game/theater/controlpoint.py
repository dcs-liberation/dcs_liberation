from __future__ import annotations

import itertools
import logging
import random
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING, Type

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
from gen.ground_forces.ai_ground_planner_db import TYPE_SHORAD
from gen.runways import RunwayAssigner, RunwayData
from gen.ground_forces.combat_stance import CombatStance
from .base import Base
from .missiontarget import MissionTarget
from .theatergroundobject import (
    BaseDefenseGroundObject,
    EwrGroundObject,
    SamGroundObject,
    TheaterGroundObject,
    VehicleGroupGroundObject, GenericCarrierGroundObject,
)
from ..weather import Conditions

if TYPE_CHECKING:
    from game import Game
    from gen.flights.flight import FlightType
    from ..event import UnitsDeliveryEvent


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
    base_garrisons: List[Point] = field(default_factory=list)

    #: Locations used for spawning air defenses for bases. Used by SAMs, AAA,
    #: and SHORADs.
    base_air_defense: List[Point] = field(default_factory=list)

    #: Locations used by EWRs.
    ewrs: List[Point] = field(default_factory=list)

    #: Locations used by non-carrier ships. Carriers and LHAs are not random.
    ships: List[Point] = field(default_factory=list)

    #: Locations used by coastal defenses.
    coastal_defenses: List[Point] = field(default_factory=list)

    #: Locations used by ground based strike objectives.
    strike_locations: List[Point] = field(default_factory=list)

    #: Locations used by offshore strike objectives.
    offshore_strike_locations: List[Point] = field(default_factory=list)

    #: Locations used by missile sites like scuds and V-2s.
    missile_sites: List[Point] = field(default_factory=list)

    #: Locations of long range SAMs which should always be spawned.
    required_long_range_sams: List[Point] = field(default_factory=list)

    #: Locations of medium range SAMs which should always be spawned.
    required_medium_range_sams: List[Point] = field(default_factory=list)

    @staticmethod
    def _random_from(points: List[Point]) -> Optional[Point]:
        """Finds, removes, and returns a random position from the given list."""
        if not points:
            return None
        point = random.choice(points)
        points.remove(point)
        return point

    def random_for(self, location_type: LocationType) -> Optional[Point]:
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


class ControlPoint(MissionTarget, ABC):

    position = None  # type: Point
    name = None  # type: str

    captured = False
    has_frontline = True

    alt = 0

    # TODO: Only airbases have IDs.
    # TODO: has_frontline is only reasonable for airbases.
    # TODO: cptype is obsolete.
    def __init__(self, cp_id: int, name: str, position: Point,
                 at: db.StartingPosition, size: int,
                 importance: float, has_frontline=True,
                 cptype=ControlPointType.AIRBASE):
        super().__init__(" ".join(re.split(r"[ \-]", name)[:2]), position)
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
        self.pending_unit_deliveries: Optional[UnitsDeliveryEvent] = None

        self.target_position: Optional[Point] = None
    
    def __repr__(self):
        return f"<{__class__}: {self.name}>"

    @property
    def ground_objects(self) -> List[TheaterGroundObject]:
        return list(
            itertools.chain(self.connected_objectives, self.base_defenses))

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
        if self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP,
                           ControlPointType.LHA_GROUP]:
            for g in self.ground_objects:
                if g.dcs_identifier == "CARRIER":
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [
                                    CVN_74_John_C__Stennis,
                                    CV_1143_5_Admiral_Kuznetsov]:
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
            if isinstance(base_defense, EwrGroundObject):
                self.preset_locations.ewrs.append(base_defense.position)
            elif isinstance(base_defense, SamGroundObject):
                self.preset_locations.base_air_defense.append(
                    base_defense.position)
            elif isinstance(base_defense, VehicleGroupGroundObject):
                self.preset_locations.base_garrisons.append(
                    base_defense.position)
            else:
                logging.error(
                    "Could not determine preset location type for "
                    f"{base_defense}. Assuming garrison type.")
                self.preset_locations.base_garrisons.append(
                    base_defense.position)
        self.base_defenses = []

    # TODO: Should be Airbase specific.
    def capture(self, game: Game, for_player: bool) -> None:
        if for_player:
            self.captured = True
        else:
            self.captured = False

        self.base.set_strength_to_minimum()

        self.base.aircraft = {}
        self.base.armor = {}

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
        assert self.pending_unit_deliveries
        on_order = 0
        for unit_bought in self.pending_unit_deliveries.units:
            if issubclass(unit_bought, FlyingType):
                on_order += self.pending_unit_deliveries.units[unit_bought]

        return PendingOccupancy(self.base.total_aircraft, on_order,
                                self.aircraft_transferring(game))

    def unclaimed_parking(self, game: Game) -> int:
        return (self.total_aircraft_parking -
                self.expected_aircraft_next_turn(game).total)

    @abstractmethod
    def active_runway(self, conditions: Conditions,
                      dynamic_runways: Dict[str, RunwayData]) -> RunwayData:
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

    def process_turn(self) -> None:
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
            return sum([v for k,v in self.pending_unit_deliveries.units.items() if k in TYPE_SHORAD])
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
    def income_per_turn(self) -> int:
        return 0


class Airfield(ControlPoint):

    def __init__(self, airport: Airport, size: int,
                 importance: float, has_frontline=True):
        super().__init__(airport.id, airport.name, airport.position, airport,
                         size, importance, has_frontline,
                         cptype=ControlPointType.AIRBASE)
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

    def active_runway(self, conditions: Conditions,
                      dynamic_runways: Dict[str, RunwayData]) -> RunwayData:
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
                                CVN_74_John_C__Stennis, LHA_1_Tarawa,
                                CV_1143_5_Admiral_Kuznetsov,
                                Type_071_Amphibious_Transport_Dock]:
                            return True
        return False

    def active_runway(self, conditions: Conditions,
                      dynamic_runways: Dict[str, RunwayData]) -> RunwayData:
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
        super().__init__(cp_id, name, at, at,
                         game.theater.conflicttheater.SIZE_SMALL, 1,
                         has_frontline=False, cptype=ControlPointType.AIRCRAFT_CARRIER_GROUP)

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
        super().__init__(cp_id, name, at, at,
                         game.theater.conflicttheater.SIZE_SMALL, 1,
                         has_frontline=False, cptype=ControlPointType.LHA_GROUP)

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
        super().__init__(cp_id, name, position, at=position,
                         size=SIZE_REGULAR, importance=IMPORTANCE_MEDIUM,
                         has_frontline=False, cptype=ControlPointType.OFF_MAP)

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

    def active_runway(self, conditions: Conditions,
                      dynamic_runways: Dict[str, RunwayData]) -> RunwayData:
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
        super().__init__(cp_id, name, at, at,
                         game.theater.conflicttheater.SIZE_SMALL, 1,
                         has_frontline=True, cptype=ControlPointType.FOB)
        self.name = name
    
    def runway_is_operational(self) -> bool:
        return False
    
    def active_runway(self, conditions: Conditions,
                      dynamic_runways: Dict[str, RunwayData]) -> RunwayData:
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
