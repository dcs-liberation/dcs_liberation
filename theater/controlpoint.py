import typing
import re

from dcs.mapping import *
from dcs.country import *
from dcs.terrain import Airport

from .theatergroundobject import TheaterGroundObject


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

    def __init__(self, id: int, name: str, position: Point, at, radials: typing.Collection[int], size: int, importance: int, has_frontline=True):
        import theater.base

        self.id = id
        self.name = " ".join(re.split(r" |-", name)[:2])
        self.full_name = name
        self.position = position
        self.at = at
        self.ground_objects = []

        self.size = size
        self.importance = importance
        self.captured = False
        self.has_frontline = has_frontline
        self.radials = radials
        self.connected_points = []
        self.base = theater.base.Base()

    @classmethod
    def from_airport(cls, airport: Airport, radials: typing.Collection[int], size: int, importance: int, has_frontline=True):
        assert airport
        return cls(airport.id, airport.name, airport.position, airport, radials, size, importance, has_frontline)

    @classmethod
    def carrier(cls, name: str, at: Point):
        import theater.conflicttheater
        return cls(0, name, at, at, theater.conflicttheater.LAND, theater.conflicttheater.SIZE_SMALL, 1)

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

