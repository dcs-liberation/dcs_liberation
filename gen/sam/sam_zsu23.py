import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZSU23Generator(AirDefenseGroupGenerator):
    """
    This generate a ZSU 23 group
    """

    name = "ZSU-23 Group"
    price = 50

    def generate(self):
        num_launchers = random.randint(4, 5)

        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SPAAA_ZSU_23_4_Shilka_Gun_Dish,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
