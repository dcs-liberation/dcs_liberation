import re
import typing
from enum import Enum

from dcs.mapping import *
from dcs.terrain import Airport
from dcs.ships import CVN_74_John_C__Stennis, LHA_1_Tarawa, CV_1143_5_Admiral_Kuznetsov

from game import db
from .theatergroundobject import TheaterGroundObject



class ControlPointType(Enum):
    AIRBASE = 0                # An airbase with slot for everything
    AIRCRAFT_CARRIER_GROUP = 1 # A group with a Stennis type carrier (F/A-18, F-14 compatible)
    LHA_GROUP = 2              # A group with a Tarawa carrier (Helicopters & Harrier)
    FARP = 4                   # A FARP, with slots for helicopters
    FOB = 5                    # A FOB (ground units only)


class ControlPoint:

    id = 0
    position = None  # type: Point
    name = None  # type: str
    full_name = None  # type: str
    base = None  # type: theater.base.Base
    at = None  # type: db.StartPosition

    connected_points = None  # type: typing.List[ControlPoint]
    ground_objects = None  # type: typing.List[TheaterGroundObject]

    captured = False
    has_frontline = True
    frontline_offset = 0.0
    cptype: ControlPointType = None

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
        self.has_frontline = has_frontline
        self.radials = radials
        self.connected_points = []
        self.base = theater.base.Base()
        self.cptype = cptype

    @classmethod
    def from_airport(cls, airport: Airport, radials: typing.Collection[int], size: int, importance: float, has_frontline=True):
        assert airport
        return cls(airport.id, airport.name, airport.position, airport, radials, size, importance, has_frontline, cptype=ControlPointType.AIRBASE)

    @classmethod
    def carrier(cls, name: str, at: Point):
        import theater.conflicttheater
        return cls(0, name, at, at, theater.conflicttheater.LAND, theater.conflicttheater.SIZE_SMALL, 1,
                   has_frontline=False, cptype=ControlPointType.AIRCRAFT_CARRIER_GROUP)

    def __str__(self):
        return self.name

    @property
    def is_global(self):
        return not self.connected_points

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

    def has_runway(self):
        """
        Check whether this control point can have aircraft taking off or landing.
        :return:
        """
        if self.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP] :
            for g in self.ground_objects:
                if g.dcs_identifier == "CARRIER":
                    for group in g.groups:
                        for u in group.units:
                            if db.unit_type_from_name(u.type) in [CVN_74_John_C__Stennis, LHA_1_Tarawa, CV_1143_5_Admiral_Kuznetsov]:
                                return True
            return False
        elif self.cptype in [ControlPointType.AIRBASE, ControlPointType.FARP]:
            return True
        else:
            return True

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

