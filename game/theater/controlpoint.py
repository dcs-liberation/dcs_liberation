from __future__ import annotations

import itertools
import re
from enum import Enum
from typing import Dict, Iterator, List, TYPE_CHECKING

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
    TheaterGroundObject,
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
        obj.airport = airport()
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

    def connect(self, to):
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

    def capture(self, game: Game, for_player: bool) -> None:
        if for_player:
            self.captured = True
        else:
            self.captured = False

        self.base.set_strength_to_minimum()

        self.base.aircraft = {}
        self.base.armor = {}

        # Handle cyclic dependency.
        from .start_generator import BaseDefenseGenerator
        self.base_defenses = []
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
