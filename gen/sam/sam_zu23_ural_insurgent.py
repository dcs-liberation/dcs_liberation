import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class ZU23UralInsurgentGenerator(GroupGenerator):
    """
    This generate a Zu23 Ural group
    """

    def generate(self):
        num_launchers = random.randint(2, 8)

        positions = self.get_circular_position(num_launchers, launcher_distance=80, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.AAA_ZU_23_Insurgent_on_Ural_375, "SPAA#" + str(i), position[0], position[1], position[2])
