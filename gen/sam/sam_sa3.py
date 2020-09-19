import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class SA3Generator(GroupGenerator):
    """
    This generate a SA-3 group
    """

    name = "SA-3/S-125 Site"

    def generate(self):
        self.add_unit(AirDefence.SAM_SR_P_19, "SR", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_SA_3_S_125_TR_SNR, "TR", self.position.x + 20, self.position.y, self.heading)

        num_launchers = random.randint(3, 6)
        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=180)

        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_SA_3_S_125_LN_5P73, "LN#" + str(i), position[0], position[1], position[2])