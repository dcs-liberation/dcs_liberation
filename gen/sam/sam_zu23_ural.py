import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZU23UralGenerator(AirDefenseGroupGenerator):
    """
    This generate a Zu23 Ural group
    """

    name = "ZU-23 Ural Group"
    price = 64

    def generate(self):
        num_launchers = 4

        positions = self.get_circular_position(
            num_launchers, launcher_distance=80, coverage=360
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Ural_375_ZU_23,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
