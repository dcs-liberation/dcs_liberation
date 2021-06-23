import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class GepardGenerator(AirDefenseGroupGenerator):
    """
    This generate a Gepard group
    """

    name = "Gepard Group"
    price = 50

    def generate(self):
        num_launchers = 2

        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Gepard,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )
        self.add_unit(
            Unarmed.M_818,
            "TRUCK",
            self.position.x + 80,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
