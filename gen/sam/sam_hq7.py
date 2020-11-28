import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class HQ7Generator(AirDefenseGroupGenerator):
    """
    This generate an HQ7 group
    """

    name = "HQ-7 Site"
    price = 120

    def generate(self):
        self.add_unit(AirDefence.HQ_7_Self_Propelled_STR, "STR", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.HQ_7_Self_Propelled_LN, "LN", self.position.x + 20, self.position.y, self.heading)

        # Triple A for close range defense
        self.add_unit(AirDefence.AAA_ZU_23_on_Ural_375, "AAA1", self.position.x + 20, self.position.y+30, self.heading)
        self.add_unit(AirDefence.AAA_ZU_23_on_Ural_375, "AAA2", self.position.x - 20, self.position.y-30, self.heading)

        num_launchers = random.randint(0, 3)
        if num_launchers > 0:
            positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=360)
            for i, position in enumerate(positions):
                self.add_unit(AirDefence.HQ_7_Self_Propelled_LN, "LN#" + str(i), position[0], position[1], position[2])

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
