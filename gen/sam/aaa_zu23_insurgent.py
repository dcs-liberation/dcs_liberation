import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZU23InsurgentGenerator(AirDefenseGroupGenerator):
    """
    This generate a ZU23 insurgent flak artillery group
    """

    name = "Zu-23 Site"
    price = 56

    def generate(self):
        index = 0
        for i in range(4):
            index = index + 1
            spacing_x = random.randint(10, 40)
            spacing_y = random.randint(10, 40)
            self.add_unit(
                AirDefence.ZU_23_Closed_Insurgent,
                "AAA#" + str(index),
                self.position.x + spacing_x * i,
                self.position.y + spacing_y * i,
                self.heading,
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
