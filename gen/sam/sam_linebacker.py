import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class LinebackerGenerator(AirDefenseGroupGenerator):
    """
    This generate an m6 linebacker group
    """

    name = "Linebacker Group"

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
                AirDefence.M6_Linebacker,
                "M6#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
