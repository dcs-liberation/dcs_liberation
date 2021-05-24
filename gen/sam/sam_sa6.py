import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA6Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-6 group
    """

    name = "SA-6 Kub Site"
    price = 102

    def generate(self):
        self.add_unit(
            AirDefence.SAM_SA_6_Kub_Straight_Flush_STR,
            "STR",
            self.position.x,
            self.position.y,
            self.heading,
        )

        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=360
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SAM_SA_6_Kub_Gainful_TEL,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
