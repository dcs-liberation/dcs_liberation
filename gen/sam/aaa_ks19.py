import random

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)
from pydcs_extensions.highdigitsams import highdigitsams


class KS19Generator(AirDefenseGroupGenerator):
    """
    This generate a KS 19 flak artillery group (KS-19 from the High Digit SAM mod)
    """

    name = "KS-19 AAA Site"

    def generate(self):
        self.add_unit(
            highdigitsams.AAA_SON_9_Fire_Can,
            "TR",
            self.position.x - 20,
            self.position.y - 20,
            self.heading,
        )

        index = 0
        for i in range(4):
            spacing_x = random.randint(10, 40)
            spacing_y = random.randint(10, 40)
            index = index + 1
            self.add_unit(
                highdigitsams.AAA_100mm_KS_19,
                "AAA#" + str(index),
                self.position.x + spacing_x * i,
                self.position.y + spacing_y * i,
                self.heading,
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
