import typing
import dcs

from .controlpoint import *

SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 2
IMPORTANCE_HIGH = 3

ALL_RADIALS = [0, 45, 90, 135, 180, 225, 270, 315, ]
COAST_VERTICAL = [45, 90, 135, ]
COAST_HORIZONTAL = [315, 0, 45, ]


class ConflictTheater:
    controlpoints = [] # type: typing.List[ControlPoint]

    def add_controlpoint(self, point: ControlPoint, connected_to: typing.Collection[ControlPoint] = []):
        for connected_point in connected_to:
            point.connect(to=connected_point)

        self.controlpoints.append(point)

    def player_bases(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if point.captured and point.base]
