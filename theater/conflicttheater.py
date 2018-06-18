import typing
import itertools

import dcs
from dcs.mapping import Point

from .landmap import ray_tracing
from .controlpoint import ControlPoint

SIZE_TINY = 150
SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 1.2
IMPORTANCE_HIGH = 1.4

ALL_RADIALS = [0, 45, 90, 135, 180, 225, 270, 315, ]
COAST_NS_E = [45, 90, 135, ]
COAST_EW_N = [315, 0, 45, ]

COAST_NS_W = [225, 270, 315, ]
COAST_EW_S = [135, 180, 225, ]

COAST_SWNE = [45, 90, 135, 180, 225, ]
COAST_SENW = [135, 180, 225, 270, 315, ]


class ConflictTheater:
    terrain = None  # type: dcs.terrain.Terrain
    controlpoints = None  # type: typing.Collection[ControlPoint]
    reference_points = None  # type: typing.Dict
    overview_image = None  # type: str
    landmap_poly = None
    daytime_map = None  # type: typing.Dict[str, typing.Tuple[int, int]]

    def __init__(self):
        self.controlpoints = []

    def add_controlpoint(self, point: ControlPoint, connected_to: typing.Collection[ControlPoint] = []):
        for connected_point in connected_to:
            point.connect(to=connected_point)

        self.controlpoints.append(point)

    def is_on_land(self, point: Point) -> bool:
        if not self.landmap_poly:
            return True

        for poly in self.landmap_poly:
            return ray_tracing(point.x, point.y, poly)

        return False

    def player_points(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if point.captured]

    def conflicts(self, from_player=True) -> typing.Collection[typing.Tuple[ControlPoint, ControlPoint]]:
        for cp in [x for x in self.controlpoints if x.captured == from_player]:
            for connected_point in [x for x in cp.connected_points if x.captured != from_player]:
                yield (cp, connected_point)

    def enemy_points(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if not point.captured]
