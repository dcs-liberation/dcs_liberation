import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class SA8Generator(GroupGenerator):
    """
    This generate a SA-8 group
    """

    def generate(self):
        self.add_unit(AirDefence.SAM_SA_8_Osa_9A33, "OSA", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_SA_8_Osa_LD_9T217, "LD", self.position.x + 20, self.position.y, self.heading)
