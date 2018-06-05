import typing
import dcs
import math

from dcs.mapping import *
from dcs.country import *

from gen.conflictgen import *


class ControlPoint:
    connected_points = []  # type: typing.List[ControlPoint]
    position = None  # type: Point
    captured = False
    base: None  # type: theater.base.Base
    at: None  # type: db.StartPosition

    def __init__(self, name: str, position: Point, at, radials: typing.Collection[int], size: int, importance: int):
        import theater.base

        self.name = name
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
        return cls(airport.name, airport.position, airport, radials, size, importance)

    def __str__(self):
        return self.name

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
        cp = from_cp  # type: ControlPoint

        attack_radial = self.find_radial(cp.position.heading_between_point(self.position))
        defense_radial = self.find_radial(self.position.heading_between_point(cp.position), ignored_radial=attack_radial)

        return Conflict.capture_conflict(attacker=attacker,
                                         attack_heading=attack_radial,
                                         defender=defender,
                                         defense_heading=defense_radial,
                                         position=self.position,
                                         size=self.size,
                                         radials=self.radials)
