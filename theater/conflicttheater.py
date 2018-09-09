import typing
import itertools

import dcs
from dcs.mapping import Point

from .landmap import Landmap, poly_contains
from .controlpoint import ControlPoint
from .theatergroundobject import TheaterGroundObject

SIZE_TINY = 150
SIZE_SMALL = 600
SIZE_REGULAR = 1000
SIZE_BIG = 2000
SIZE_LARGE = 3000

IMPORTANCE_LOW = 1
IMPORTANCE_MEDIUM = 1.2
IMPORTANCE_HIGH = 1.4

"""
ALL_RADIALS = [0, 45, 90, 135, 180, 225, 270, 315, ]
COAST_NS_E = [45, 90, 135, ]
COAST_EW_N = [315, 0, 45, ]
COAST_NSEW_E = [225, 270, 315, ]
COAST_NSEW_W = [45, 90, 135, ]

COAST_NS_W = [225, 270, 315, ]
COAST_EW_S = [135, 180, 225, ]
"""

LAND = [0, 45, 90, 135, 180, 225, 270, 315, ]

COAST_V_E = [0, 45, 90, 135, 180]
COAST_V_W = [180, 225, 270, 315, 0]

COAST_A_W = [315, 0, 45,  135, 180, 225, 270]
COAST_A_E = [0, 45, 90, 135, 180, 225, 315]

COAST_H_N = [270, 315, 0, 45, 90]
COAST_H_S = [90, 135, 180, 225, 270]

COAST_DL_E = [45, 90, 135, 180, 225]
COAST_DL_W = [225, 270, 315, 0, 45]
COAST_DR_E = [315, 0, 45, 90, 135]
COAST_DR_W = [135, 180, 225, 315]


class ConflictTheater:
    terrain = None  # type: dcs.terrain.Terrain
    controlpoints = None  # type: typing.Collection[ControlPoint]

    reference_points = None  # type: typing.Dict
    overview_image = None  # type: str
    landmap = None  # type: landmap.Landmap
    daytime_map = None  # type: typing.Dict[str, typing.Tuple[int, int]]

    def __init__(self):
        self.controlpoints = []

    def set_groundobject(self, dictionary: typing.Dict[int, typing.Collection[TheaterGroundObject]]):
        for id, value in dictionary.items():
            for cp in self.controlpoints:
                if cp.id == id:
                    cp.ground_objects = value
                    break

    def add_controlpoint(self, point: ControlPoint, connected_to: typing.Collection[ControlPoint] = []):
        for connected_point in connected_to:
            point.connect(to=connected_point)

        self.controlpoints.append(point)

    def is_on_land(self, point: Point) -> bool:
        if not self.landmap:
            return True

        # check first poly (main land poly)
        if not poly_contains(point.x, point.y, self.landmap[0]):
            return False

        # check others polys (exclusion zones from main)
        for poly in self.landmap[1:]:
            if poly_contains(point.x, point.y, poly):
                # point is in one of the exclusion zones, meaning that it's in the lake or something
                return False

        return True

    def player_points(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if point.captured]

    def conflicts(self, from_player=True) -> typing.Collection[typing.Tuple[ControlPoint, ControlPoint]]:
        for cp in [x for x in self.controlpoints if x.captured == from_player]:
            for connected_point in [x for x in cp.connected_points if x.captured != from_player]:
                yield (cp, connected_point)

    def enemy_points(self) -> typing.Collection[ControlPoint]:
        return [point for point in self.controlpoints if not point.captured]
