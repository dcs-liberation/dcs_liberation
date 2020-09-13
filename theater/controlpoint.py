import re
import typing
from enum import Enum

from dcs.mapping import *
from dcs.ships import (
    CVN_74_John_C__Stennis,
    CV_1143_5_Admiral_Kuznetsov,
    LHA_1_Tarawa,
    Type_071_Amphibious_Transport_Dock,
)
from dcs.terrain.terrain import Airport

from game import db
from gen.ground_forces.combat_stance import CombatStance
from .missiontarget import MissionTarget
from .theatergroundobject import TheaterGroundObject


class ControlPointType(Enum):
    AIRBASE = 0                # An airbase with slots for everything
    AIRCRAFT_CARRIER_GROUP = 1 # A group with a Stennis type carrier (F/A-18, F-14 compatible)
    LHA_GROUP = 2              # A group with a Tarawa carrier (Helicopters & Harrier)
    FARP = 4                   # A FARP, with slots for helicopters
    FOB = 5                    # A FOB (ground units only)


class ControlPoint(MissionTarget):

    id = 0
    position = None  # type: Point
    name = None  # type: str
    full_name = None  # type: str
    base = None  # type: theater.base.Base
    at = None  # type: db.StartPosition
    allow_sea_units = True

    connected_points = None  # type: typing.List[ControlPoint]
    ground_objects = None  # type: typing.List[TheaterGroundObject]

    captured = False
    has_frontline = True
    frontline_offset = 0.0
    cptype: ControlPointType = None

    alt = 0

    def __init__(self, id: int, name: str, position: Point, at, radials: typing.Collection[int], size: int, importance: float,
                 has_frontline=True, cptype=ControlPointType.AIRBASE):
        import theater.base

        self.id = id
        self.name = " ".join(re.split(r" |-", name)[:2])
        self.full_name = name
        self.position = position
        self.at = at
        self.ground_objects = []
        self.ships = []

        self.size = size
        self.importance = importance
        self.captured = False
        self.captured_invert = False
        self.has_frontline = has_frontline
        self.radials = radials
        self.connected_points = []
        self.base = theater.base.Base()
        self.cptype = cptype
        self.stances = {}
        self.airport = None

    @classmethod
    def from_airport(cls, airport: Airport, radials: typing.Collection[int], size: int, importance: float, has_frontline=True):
        assert airport
        obj = cls(airport.id, airport.name, airport.position, airport, radials, size, importance, has_frontline, cptype=ControlPointType.AIRBASE)
        obj.airport = airport()
        return obj

    @classmethod
    def carrier(cls, name: str, at: Point, id: int):
        import theater.conflicttheater
        cp = cls(id, name, at, at, theater.conflicttheater.LAND, theater.conflicttheater.SIZE_SMALL, 1,
                   has_frontline=False, cptype=ControlPointType.AIRCRAFT_CARRIER_GROUP)
        return cp

    @classmethod
    def lha(cls, name: str, at: Point, id: int):
        import theater.conflicttheater
        cp = cls(id, name, at, at, theater.conflicttheater.LAND, theater.conflicttheater.SIZE_SMALL, 1,
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
        return self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]

    @property
    def is_fleet(self):
        return self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]

    @property
    def is_lha(self):
        return self.cptype in [ControlPointType.LHA_GROUP]

    @property
    def sea_radials(self) -> typing.Collection[int]:
        # TODO: fix imports
        all_radials = [0, 45, 90, 135, 180, 225, 270, 315, ]
        result = []
        for r in all_radials:
            if r not in self.radials:
                result.append(r)
        return result

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

    def find_radial(self, heading: int, ignored_radial: int = None):
        closest_radial = 0
        closest_radial_delta = 360
        for radial in [x for x in self.radials if x != ignored_radial]:
            delta = math.fabs(radial - heading)
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
