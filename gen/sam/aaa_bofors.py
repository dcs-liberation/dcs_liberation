import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class BoforsGenerator(AirDefenseGroupGenerator):
    """
    This generate a Bofors flak artillery group
    """

    name = "Bofors AAA"

    def generate(self) -> None:

        index = 0
        for i in range(4):
            spacing_x = random.randint(10, 40)
            spacing_y = random.randint(10, 40)
            index = index + 1
            self.add_unit(
                AirDefence.Bofors40,
                "AAA#" + str(index),
                self.position.x + spacing_x * i,
                self.position.y + spacing_y * i,
                self.heading,
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
