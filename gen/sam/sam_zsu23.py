import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class ZSU23Generator(GroupGenerator):
    """
    This generate a ZSU 23 group
    """

    name = "ZSU-23 Group"

    def generate(self):
        num_launchers = random.randint(2, 5)

        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=180)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SPAAA_ZSU_23_4_Shilka, "SPAA#" + str(i), position[0], position[1], position[2])
