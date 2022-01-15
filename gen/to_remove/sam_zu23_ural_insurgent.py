from dcs.vehicles import AirDefence

from game.theater.theatergroundobject import AirDefenseRange
from gen.to_remove.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
)


class ZU23UralInsurgentGenerator(AirDefenseGroupGenerator):
    """
    This generate a Zu23 Ural group
    """

    name = "ZU-23 Ural Insurgent Group"

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA

    def generate(self) -> None:
        num_launchers = 4

        positions = self.get_circular_position(
            num_launchers, launcher_distance=80, coverage=360
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Ural_375_ZU_23_Insurgent,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )
