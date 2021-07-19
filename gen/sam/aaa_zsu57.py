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

    def generate(self) -> None:
        num_launchers = 4
        positions = self.get_circular_position(
            num_launchers, launcher_distance=110, coverage=360
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.ZSU_57_2,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
