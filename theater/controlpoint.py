import typing
import dcs

from dcs.mapping import *
from dcs.country import *

from gen.conflictgen import Conflict
from .base import *

class ControlPoint:
    connected_points = [] # type: typing.Collection[ControlPoint]
    point = None # type: Point
    captured = False
    base = None # type: Base

    def __init__(self, point: Point, size: int, importance: int, captured: bool, base: Base):
        self.point = point
        self.size = size
        self.importance = importance
        self.captured = captured
        self.base = base

    def connect(self, to):
        self.connected_points.append(to)

    def conflict_attack(self, x, attacker: Country, defender: Country) -> Conflict:
        #heading = heading_between_points(self.point.x, self.point.y, x.point.x, x.point.y)
        return Conflict(attacker, 0, defender, 90, self.point, self.size)


