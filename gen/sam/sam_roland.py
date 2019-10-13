from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator


class RolandGenerator(GroupGenerator):
    """
    This generate a Roland group
    """

    def generate(self):
        self.add_unit(AirDefence.SAM_Roland_ADS, "ADS", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Roland_EWR, "EWR", self.position.x + 40, self.position.y, self.heading)
        self.add_unit(Unarmed.Transport_M818, "TRUCK", self.position.x + 80, self.position.y, self.heading)

