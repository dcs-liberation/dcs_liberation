from dcs import Point


class PointWithHeading(Point):
    def __init__(self):
        super(PointWithHeading, self).__init__(0, 0)
        self.heading = 0

    @staticmethod
    def from_point(point: Point, heading: int):
        p = PointWithHeading()
        p.x = point.x
        p.y = point.y
        p.heading = heading
        return p
