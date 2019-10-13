import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator


class GepardGenerator(GroupGenerator):
    """
    This generate a Gepard group
    """

    def generate(self):
        self.add_unit(AirDefence.SPAAA_Gepard, "SPAAA", self.position.x, self.position.y, self.heading)
        if random.randint(0, 1) == 1:
            self.add_unit(AirDefence.SPAAA_Gepard, "SPAAA2", self.position.x, self.position.y, self.heading)
        self.add_unit(Unarmed.Transport_M818, "TRUCK", self.position.x + 80, self.position.y, self.heading)

