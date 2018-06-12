import typing
import itertools

import dcs

from .controlpoint import *

SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 1.2
IMPORTANCE_HIGH = 1.4

ALL_RADIALS = [0, 45, 90, 135, 180, 225, 270, 315, ]
COAST_VERTICAL = [45, 90, 135, ]
COAST_HORIZONTAL = [315, 0, 45, ]


class ConflictTheater:
    controlpoints = None  # type: typing.Collection[ControlPoint]
    reference_points = None  # type: typing.Dict

    def __init__(self):
        self.controlpoints = []

    def add_controlpoint(self, point: ControlPoint, connected_to: typing.Collection[ControlPoint] = []):
        for connected_point in connected_to:
            point.connect(to=connected_point)

        self.controlpoints.append(point)

    def player_points(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if point.captured]

    def conflicts(self, from_player=True) -> typing.Collection[typing.Tuple[ControlPoint, ControlPoint]]:
        for cp in [x for x in self.controlpoints if x.captured == from_player]:
            for connected_point in [x for x in cp.connected_points if x.captured != from_player]:
                yield (cp, connected_point)

    def enemy_points(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if not point.captured]
