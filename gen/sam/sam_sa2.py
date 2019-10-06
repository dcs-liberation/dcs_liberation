import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import AntiAirGroupGenerator


class SA2Generator(AntiAirGroupGenerator):
    """
    This generate a SA-2 group
    """

    def generate(self):
        self.add_unit(AirDefence.SAM_SR_P_19, "SR", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_SA_2_TR_SNR_75_Fan_Song, "TR", self.position.x + 20, self.position.y, self.heading)

        num_launchers = random.randint(3, 6)
        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=180)

        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_SA_2_LN_SM_90, "LN#" + str(i), position[0], position[1], position[2])