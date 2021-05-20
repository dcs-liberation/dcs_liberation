import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZU23UralInsurgentGenerator(AirDefenseGroupGenerator):
    """
    This generate a Zu23 Ural group
    """

    name = "ZU-23 Ural Insurgent Group"
    price = 64

    def generate(self):
        num_launchers = random.randint(2, 8)

        positions = self.get_circular_position(
            num_launchers, launcher_distance=80, coverage=360
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SPAAA_ZU_23_2_Insurgent_Mounted_Ural_375,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
