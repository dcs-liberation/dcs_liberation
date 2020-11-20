from __future__ import annotations

import itertools
import logging
import random
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterator, List, Optional, TYPE_CHECKING

from dcs.mapping import Point
from dcs.ships import (
    CVN_74_John_C__Stennis,
    CV_1143_5_Admiral_Kuznetsov,
    LHA_1_Tarawa,
    Type_071_Amphibious_Transport_Dock,
)
from dcs.terrain.terrain import Airport

from game import db
from gen.ground_forces.combat_stance import CombatStance
from .base import Base
from .missiontarget import MissionTarget
from .theatergroundobject import (
    BaseDefenseGroundObject,
    EwrGroundObject,
    SamGroundObject,
    TheaterGroundObject,
    VehicleGroupGroundObject,
)

if TYPE_CHECKING:
    from game import Game
    from gen.flights.flight import FlightType


class ControlPointType(Enum):
    AIRBASE = 0                # An airbase with slots for everything
    AIRCRAFT_CARRIER_GROUP = 1 # A group with a Stennis type carrier (F/A-18, F-14 compatible)
    LHA_GROUP = 2              # A group with a Tarawa carrier (Helicopters & Harrier)
    FARP = 4                   # A FARP, with slots for helicopters
    FOB = 5                    # A FOB (ground units only)


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

    #: Locations used by SAMs outside of bases.
    sams: List[Point] = field(default_factory=list)

    #: Locations used by non-carrier ships. Carriers and LHAs are not random.
    ships: List[Point] = field(default_factory=list)

    #: Locations used by coastal defenses.
    coastal_defenses: List[Point] = field(default_factory=list)

    #: Locations used by ground based strike objectives.
    strike_locations: List[Point] = field(default_factory=list)

    #: Locations used by offshore strike objectives.
    offshore_strike_locations: List[Point] = field(default_factory=list)

    #: Locations of SAMs which should always be spawned.
    required_sams: List[Point] = field(default_factory=list)

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
        if location_type == LocationType.Garrison:
            return self._random_from(self.base_garrisons)
        if location_type == LocationType.Sam:
            return self._random_from(self.sams)
        if location_type == LocationType.BaseAirDefense:
            return self._random_from(self.base_air_defense)
        if location_type == LocationType.Ewr:
            return self._random_from(self.ewrs)
        if location_type == LocationType.Shorad:
            return self._random_from(self.base_garrisons)
        if location_type == LocationType.OffshoreStrikeTarget:
            return self._random_from(self.offshore_strike_locations)
        if location_type == LocationType.Ship:
            return self._random_from(self.ships)
        if location_type == LocationType.StrikeTarget:
            return self._random_from(self.strike_locations)
        logging.error(f"Unknown location type: {location_type}")
        return None


class ControlPoint(MissionTarget):

    position = None  # type: Point
    name = None  # type: str

    captured = False
    has_frontline = True
    frontline_offset = 0.0

    alt = 0

    def __init__(self, id: int, name: str, position: Point,
                 at: db.StartingPosition, radials: List[int], size: int,
                 importance: float, has_frontline=True,
                 cptype=ControlPointType.AIRBASE):
        super().__init__(" ".join(re.split(r" |-", name)[:2]), position)
        self.id = id
        self.full_name = name
        self.at = at
        self.connected_objectives: List[TheaterGroundObject] = []
        self.base_defenses: List[BaseDefenseGroundObject] = []
        self.preset_locations = PresetLocations()

        self.size = size
        self.importance = importance
        self.captured = False
        self.captured_invert = False
        self.has_frontline = has_frontline
        self.radials = radials
        self.connected_points: List[ControlPoint] = []
        self.base: Base = Base()
        self.cptype = cptype
        self.stances: Dict[int, CombatStance] = {}
        self.airport = None

    @property
    def ground_objects(self) -> List[TheaterGroundObject]:
        return list(
            itertools.chain(self.connected_objectives, self.base_defenses))

    @classmethod
    def from_airport(cls, airport: Airport, radials: List[int], size: int, importance: float, has_frontline=True):
        assert airport
        obj = cls(airport.id, airport.name, airport.position, airport, radials, size, importance, has_frontline, cptype=ControlPointType.AIRBASE)
        obj.airport = airport
        return obj

    @classmethod
    def carrier(cls, name: str, at: Point, id: int):
        import game.theater.conflicttheater
        cp = cls(id, name, at, at, game.theater.conflicttheater.LAND, game.theater.conflicttheater.SIZE_SMALL, 1,
                 has_frontline=False, cptype=ControlPointType.AIRCRAFT_CARRIER_GROUP)
        return cp

    @classmethod
    def lha(cls, name: str, at: Point, id: int):
        import game.theater.conflicttheater
        cp = cls(id, name, at, at, game.theater.conflicttheater.LAND, game.theater.conflicttheater.SIZE_SMALL, 1,
                 has_frontline=False, cptype=ControlPointType.LHA_GROUP)
        return cp

    @property
    def heading(self):
        if self.cptype == ControlPointType.AIRBASE:
            return self.airport.runways[0].heading
        elif self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]:
            return 0 # TODO compute heading
        else:
            return 0

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
        return self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]

    @property
    def is_fleet(self):
        """
        :return: Whether this control point is a boat (mobile)
        """
        return self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]

    @property
    def is_lha(self):
        """
        :return: Whether this control point is an LHA
        """
        return self.cptype in [ControlPointType.LHA_GROUP]

    @property
    def sea_radials(self) -> List[int]:
        # TODO: fix imports
        all_radials = [0, 45, 90, 135, 180, 225, 270, 315, ]
        result = []
        for r in all_radials:
            if r not in self.radials:
                result.append(r)
        return result

    @property
    def available_aircraft_slots(self):
        """
        :return: The maximum number of aircraft that can be stored in this control point
        """
        if self.cptype == ControlPointType.AIRBASE:
            return len(self.airport.parking_slots)
        elif self.is_lha:
            return 20
        elif self.is_carrier:
            return 90
        else:
            return 0

    def connect(self, to: ControlPoint) -> None:
        self.connected_points.append(to)
        self.stances[to.id] = CombatStance.DEFENSIVE

    def has_runway(self):
        """
        Check whether this control point can have aircraft taking off or landing.
        :return:
        """
        if self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP] :
            for g in self.ground_objects:
                if g.dcs_identifier in ["CARRIER", "LHA"]:
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [CVN_74_John_C__Stennis, LHA_1_Tarawa, CV_1143_5_Admiral_Kuznetsov, Type_071_Amphibious_Transport_Dock]:
                                return True
            return False
        elif self.cptype in [ControlPointType.AIRBASE, ControlPointType.FARP]:
            return True
        else:
            return True

    def get_carrier_group_name(self):
        """
        Get the carrier group name if the airbase is a carrier
        :return: Carrier group name
        """
        if self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP] :
            for g in self.ground_objects:
                if g.dcs_identifier == "CARRIER":
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [CVN_74_John_C__Stennis, CV_1143_5_Admiral_Kuznetsov]:
                                return group.name
                elif g.dcs_identifier == "LHA":
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [LHA_1_Tarawa]:
                                return group.name
        return None

    def is_connected(self, to) -> bool:
        return to in self.connected_points

    def find_radial(self, heading: int, ignored_radial: int = None) -> int:
        closest_radial = 0
        closest_radial_delta = 360
        for radial in [x for x in self.radials if x != ignored_radial]:
            delta = abs(radial - heading)
            if delta < closest_radial_delta:
                closest_radial = radial
                closest_radial_delta = delta

        return closest_radial

    def find_ground_objects_by_obj_name(self, obj_name):
        found = []
        for g in self.ground_objects:
            if g.obj_name == obj_name:
                found.append(g)
        return found

    def is_friendly(self, to_player: bool) -> bool:
        return self.captured == to_player

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

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        yield from super().mission_types(for_player)
        if self.is_friendly(for_player):
            if self.is_fleet:
                yield from [
                    # TODO: FlightType.INTERCEPTION
                    # TODO: Buddy tanking for the A-4?
                    # TODO: Rescue chopper?
                    # TODO: Inter-ship logistics?
                ]
            else:
                yield from [
                    # TODO: FlightType.INTERCEPTION
                    # TODO: FlightType.LOGISTICS
                ]
        else:
            if self.is_fleet:
                yield FlightType.ANTISHIP
            else:
                yield from [
                    # TODO: FlightType.STRIKE
                ]
