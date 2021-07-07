from game.point_with_heading import PointWithHeading


class ArmorGroupLocation:
    def __init__(self, PointWithHeading, bool):
        self.position = PointWithHeading
        self.shoradIncluded = bool
