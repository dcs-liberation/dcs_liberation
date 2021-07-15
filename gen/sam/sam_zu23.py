import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZU23Generator(AirDefenseGroupGenerator):
    """
    This generate a ZU23 flak artillery group
    """

    name = "ZU-23 Group"

    def generate(self) -> None:
        index = 0
        for i in range(4):
            index = index + 1
            spacing_x = random.randint(10, 40)
            spacing_y = random.randint(10, 40)
            self.add_unit(
                AirDefence.ZU_23_Emplacement_Closed,
                "AAA#" + str(index),
                self.position.x + spacing_x * i,
                self.position.y + spacing_y * i,
                self.heading,
            )
        self.add_unit(
            Unarmed.M_818,
            "TRUCK",
            self.position.x + 80,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
