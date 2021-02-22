import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ChaparralGenerator(AirDefenseGroupGenerator):
    """
    This generate a Chaparral group
    """

    name = "Chaparral Group"
    price = 66

    def generate(self):
        num_launchers = random.randint(2, 4)

        self.add_unit(
            Unarmed.Transport_M818,
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
                AirDefence.SAM_Chaparral_M48,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
