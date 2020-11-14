import random

from dcs.vehicles import AirDefence

from gen.sam.genericsam_group_generator import GenericSamGroupGenerator


class SA11Generator(GenericSamGroupGenerator):
    """
    This generate a SA-11 group
    """

    name = "SA-11 Buk Battery"
    price = 180

    def generate(self):
        self.add_unit(AirDefence.SAM_SA_11_Buk_SR_9S18M1, "SR", self.position.x+20, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_SA_11_Buk_CC_9S470M1, "CC", self.position.x, self.position.y, self.heading)

        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=140, coverage=180)

        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_SA_11_Buk_LN_9A310M1, "LN#" + str(i), position[0], position[1], position[2])