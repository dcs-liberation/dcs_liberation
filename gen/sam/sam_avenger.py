import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator


class AvengerGenerator(GroupGenerator):
    """
    This generate an Avenger group
    """

    name = "Avenger Group"
    price = 62

    def generate(self):
        num_launchers = random.randint(2, 3)

        self.add_unit(Unarmed.Transport_M818, "TRUCK", self.position.x, self.position.y, self.heading)
        positions = self.get_circular_position(num_launchers, launcher_distance=110, coverage=180)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_Avenger_M1097, "SPAA#" + str(i), position[0], position[1], position[2])
