from __future__ import annotations

import math

from dcs import Point
from dcs.terrain import Terrain

from game.utils import Heading


class PointWithHeading(Point):
    def __init__(self, x: float, y: float, heading: Heading, terrain: Terrain) -> None:
        super().__init__(x, y, terrain)
        self.heading: Heading = heading

    @staticmethod
    def from_point(point: Point, heading: Heading) -> PointWithHeading:
        return PointWithHeading(point.x, point.y, heading, point._terrain)

    def rotate(self, origin: Point, heading: Heading) -> None:
        """Rotates the Point by a given angle clockwise around the origin"""
        ox, oy = origin.x, origin.y
        px, py = self.x, self.y
        radians = heading.radians

        self.x = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
        self.y = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
