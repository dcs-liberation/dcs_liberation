from dcs import Point
from game.utils import Heading


class PointWithHeading(Point):
    def __init__(self):
        super(PointWithHeading, self).__init__(0, 0)
        self.heading: Heading = Heading.from_degrees(0)

    @staticmethod
    def from_point(point: Point, heading: Heading):
        p = PointWithHeading()
        p.x = point.x
        p.y = point.y
        p.heading = heading
        return p
