import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class AvengerGenerator(AirDefenseGroupGenerator):
    """
    This generate an Avenger group
    """

    name = "Avenger Group"
    price = 62

    def generate(self):
        num_launchers = random.randint(2, 3)

        self.add_unit(
            Unarmed.Truck_M818_6x6,
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
                AirDefence.SAM_Avenger__Stinger,
                "SPAA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
