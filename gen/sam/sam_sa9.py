import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA9Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-9 group
    """

    name = "SA-9 Group"
    price = 40

    def generate(self):
        self.add_unit(
            Unarmed.LUV_UAZ_469_Jeep,
            "UAZ",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            Unarmed.Truck_KAMAZ_43101,
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
                AirDefence.SAM_SA_9_Strela_1_Gaskin_TEL,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
