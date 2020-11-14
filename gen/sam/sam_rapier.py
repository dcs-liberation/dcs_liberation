import random

from dcs.vehicles import AirDefence

from gen.sam.genericsam_group_generator import GenericSamGroupGenerator


class RapierGenerator(GenericSamGroupGenerator):
    """
    This generate a Rapier Group
    """

    name = "Rapier AA Site"
    price = 50

    def generate(self):
        self.add_unit(AirDefence.Rapier_FSA_Blindfire_Tracker, "BT", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.Rapier_FSA_Optical_Tracker, "OT", self.position.x + 20, self.position.y, self.heading)

        num_launchers = random.randint(3, 6)
        positions = self.get_circular_position(num_launchers, launcher_distance=80, coverage=240)

        for i, position in enumerate(positions):
            self.add_unit(AirDefence.Rapier_FSA_Launcher, "LN#" + str(i), position[0], position[1], position[2])