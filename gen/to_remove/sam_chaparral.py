from dcs.vehicles import AirDefence, Unarmed

from game.theater.theatergroundobject import AirDefenseRange
from gen.to_remove.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
)


class ChaparralGenerator(AirDefenseGroupGenerator):
    """
    This generate a Chaparral group
    """

    name = "Chaparral Group"

    def generate(self) -> None:
        num_launchers = 2

        self.add_unit(
            Unarmed.M_818,
            "TRUCK",
            self.position.x,
            self.position.y,
            self.heading,
        )
        positions = self.get_circular_position(
            num_launchers, launcher_distance=110, coverage=180
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.M48_Chaparral,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
