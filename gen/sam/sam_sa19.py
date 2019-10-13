import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class SA19Generator(GroupGenerator):
    """
    This generate a SA-19 group
    """

    def generate(self):
        num_launchers = random.randint(1, 3)

        if num_launchers == 1:
            self.add_unit(AirDefence.SAM_SA_19_Tunguska_2S6, "LN#0", self.position.x, self.position.y, self.heading)
        else:
            positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=180)
            for i, position in enumerate(positions):
                self.add_unit(AirDefence.SAM_SA_19_Tunguska_2S6, "LN#" + str(i), position[0], position[1], position[2])
