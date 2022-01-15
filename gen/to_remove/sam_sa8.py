from dcs.vehicles import AirDefence

from game.theater.theatergroundobject import AirDefenseRange
from gen.to_remove.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
)


class SA8Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-8 group
    """

    name = "SA-8 OSA Site"

    def generate(self) -> None:
        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Osa_9A33_ln,
                "OSA" + str(i),
                position[0],
                position[1],
                position[2],
            )
        self.add_unit(
            AirDefence.SA_8_Osa_LD_9T217,
            "LD",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
