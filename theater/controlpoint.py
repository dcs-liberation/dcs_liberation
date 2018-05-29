import typing
import dcs
import math

from dcs.mapping import *
from dcs.country import *

from gen.conflictgen import Conflict

class ControlPoint:
    connected_points = [] # type: typing.List[ControlPoint]
    position = None # type: Point
    captured = False
    strength = 100
    base: None # type: theater.base.Base

    def __init__(self, point: Point, radials: typing.Collection[int], size: int, importance: int):
        import theater.base

        self.position = point
        self.size = size
        self.importance = importance
        self.captured = False
        self.radials = radials
        self.base = theater.base.Base()

    def connect(self, to):
        self.connected_points.append(to)

    def find_radial(self, heading: int):
        closest_radial = 0
        closest_radial_delta = 360
        for radial in self.radials:
            delta = math.fabs(radial - heading)
            if closest_radial_delta < delta:
                closest_radial = radial
                closest_radial_delta = delta

        return closest_radial

    def conflict_attack(self, from_cp, attacker: Country, defender: Country) -> Conflict:
        cp = from_cp # type: ControlPoint

        attack_radial = self.find_radial(cp.position.heading_between_point(self.position))
        defense_radial = self.find_radial(self.position.heading_between_point(cp.position))

        return Conflict(attacker=attacker,
                        attack_heading=attack_radial,
                        defender=defender,
                        defense_heading=defense_radial,
                        position=self.position,
                        size=self.size)


