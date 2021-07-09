from game.point_with_heading import PointWithHeading


class armorgrouplocation:
    def __init__(self, point_with_heading: PointWithHeading, shorad_included: bool):
        self.position = point_with_heading
        self.shorad_included = shorad_included
