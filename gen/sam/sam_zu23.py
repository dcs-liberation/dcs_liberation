import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class ZU23Generator(AirDefenseGroupGenerator):
    """
    This generate a ZU23 flak artillery group
    """

    name = "ZU-23 Group"
    price = 54

    def generate(self):
        grid_x = random.randint(2, 3)
        grid_y = random.randint(2, 3)

        spacing = random.randint(10, 40)

        index = 0
<<<<<<< HEAD
        for i in range(2):
            index = index + 1
            spacing_x = random.randint(10, 40)
            spacing_y = random.randint(10, 40)
            self.add_unit(
                AirDefence.ZU_23_Emplacement_Closed,
                "AAA#" + str(index),
                self.position.x + spacing_x * i,
                self.position.y + spacing_y * i,
                self.heading,
            )
        self.add_unit(
            Unarmed.M_818,
            "TRUCK",
            self.position.x + 80,
            self.position.y,
            self.heading,
        )
=======
        for i in range(grid_x):
            for j in range(grid_y):
                index = index + 1
                self.add_unit(
                    AirDefence.ZU_23_Emplacement_Closed,
                    "AAA#" + str(index),
                    self.position.x + spacing * i,
                    self.position.y + spacing * j,
                    self.heading,
                )
>>>>>>> parent of 33bccd7c (removed random sam count)

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
