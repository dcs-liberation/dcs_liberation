from typing import Optional

from dcs import Point
from dcs.unitgroup import StaticGroup

from game.point_with_heading import PointWithHeading
from game.utils import Heading


class Helipad(PointWithHeading):
    def __init__(self):
        super(Helipad, self).__init__()
        self.heading = Heading.from_degrees(0)
        self.occupied = False
        self.static_unit: Optional[StaticGroup] = None

    @staticmethod
    def from_point(point: Point, heading: Heading) -> "Helipad":
        h = Helipad()
        h.x = point.x
        h.y = point.y
        h.heading = heading
        return h
