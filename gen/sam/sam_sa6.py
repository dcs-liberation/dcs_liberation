import random

from dcs.vehicles import AirDefence

from gen.sam.genericsam_group_generator import GenericSamGroupGenerator


class SA6Generator(GenericSamGroupGenerator):
    """
    This generate a SA-6 group
    """

    name = "SA-6 Kub Site"
    price = 102

    def generate(self):
        self.add_unit(AirDefence.SAM_SA_6_Kub_STR_9S91, "STR", self.position.x, self.position.y, self.heading)

        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=360)

        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_SA_6_Kub_LN_2P25, "LN#" + str(i), position[0], position[1], position[2])