from typing import Optional

from dcs.unitgroup import StaticGroup

from game.point_with_heading import PointWithHeading


class Helipad(PointWithHeading):
    def __init__(self):
        super(Helipad, self).__init__()
        self.heading = 0
        self.occupied = False
        self.static_unit: Optional[StaticGroup] = None
