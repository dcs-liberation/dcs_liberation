from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZSU57Generator(AirDefenseGroupGenerator):
    """
    This generate a Zsu 57 group
    """

    name = "ZSU-57-2 Group"
    price = 60

    def generate(self):
        num_launchers = 5
        positions = self.get_circular_position(num_launchers, launcher_distance=110, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.AAA_ZSU_57_2, "SPAA#" + str(i), position[0], position[1], position[2])

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
