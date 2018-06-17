import typing
import re

from dcs.mapping import *
from dcs.country import *
from dcs.terrain import Airport

from gen.conflictgen import Conflict


class ControlPoint:
    connected_points = []  # type: typing.List[ControlPoint]
    position = None  # type: Point
    captured = False
    base: None  # type: theater.base.Base
    at: None  # type: db.StartPosition

    def __init__(self, name: str, position: Point, at, radials: typing.Collection[int], size: int, importance: int):
        import theater.base

        self.name = " ".join(re.split(r" |-", name)[:2])
        self.full_name = name
        self.position = position
        self.at = at

        self.size = size
        self.importance = importance
        self.captured = False
        self.radials = radials
        self.connected_points = []
        self.base = theater.base.Base()

    @classmethod
    def from_airport(cls, airport: Airport, radials: typing.Collection[int], size: int, importance: int):
        assert airport
        return cls(airport.name, airport.position, airport, radials, size, importance)

    @classmethod
    def carrier(cls, name: str, at: Point):
        import theater.conflicttheater
        return cls(name, at, at, theater.conflicttheater.ALL_RADIALS, theater.conflicttheater.SIZE_SMALL, 1)

    def __str__(self):
        return self.name

    @property
    def is_global(self):
        return not self.connected_points

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

    def conflict_attack(self, from_cp, attacker: Country, defender: Country) -> Conflict:
        attack_radial = self.find_radial(self.position.heading_between_point(from_cp.position))
        defense_radial = self.find_radial(from_cp.position.heading_between_point(self.position), ignored_radial=attack_radial)

        pos = self.position.point_from_heading(0, 1000)
        return Conflict.capture_conflict(attacker=attacker,
                                         attack_heading=attack_radial,
                                         defender=defender,
                                         defense_heading=defense_radial,
                                         position=pos,
                                         size=self.size,
                                         radials=self.radials)
