from game.theater import ControlPoint


class FrontlineData:
    """
    This Data structure will store information about an existing frontline
    """

    def __init__(self, from_cp: ControlPoint, to_cp: ControlPoint):
        self.to_cp = to_cp
        self.from_cp = from_cp
        self.enemy_units_position = []
        self.blue_units_position = []
