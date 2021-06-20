import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA13Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-13 group
    """

    name = "SA-13 Strela Group"
    price = 50

    def generate(self):
        self.add_unit(
            Unarmed.UAZ_469,
            "UAZ",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            Unarmed.KAMAZ_Truck,
            "TRUCK",
            self.position.x + 40,
            self.position.y,
            self.heading,
        )

        num_launchers = random.randint(2, 3)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=360
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Strela_10M3,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
