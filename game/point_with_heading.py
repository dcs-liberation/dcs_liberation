from __future__ import annotations

import math

from dcs import Point
from game.utils import Heading


class PointWithHeading(Point):
    def __init__(self) -> None:
        super(PointWithHeading, self).__init__(0, 0)
        self.heading: Heading = Heading.from_degrees(0)

    @staticmethod
    def from_point(point: Point, heading: Heading) -> PointWithHeading:
        p = PointWithHeading()
        p.x = point.x
        p.y = point.y
        p.heading = heading
        return p

    def rotate(self, origin: Point, heading: Heading) -> None:
        """Rotates the Point by a given angle clockwise around the origin"""
        ox, oy = origin.x, origin.y
        px, py = self.x, self.y
        radians = heading.radians

        self.x = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
        self.y = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
