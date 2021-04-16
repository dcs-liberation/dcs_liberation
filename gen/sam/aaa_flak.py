import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)

GFLAK = [
    AirDefence.AAA_Flak_Vierling_38_Quad_20mm,
    AirDefence.AAA_8_8cm_Flak_18,
    AirDefence.AAA_8_8cm_Flak_36,
    AirDefence.AAA_8_8cm_Flak_37,
    AirDefence.AAA_8_8cm_Flak_41,
    AirDefence.AAA_Flak_38_20mm,
]


class FlakGenerator(AirDefenseGroupGenerator):
    """
    This generate a German flak artillery group
    """

    name = "Flak Site"
    price = 135

    def generate(self):
        grid_x = random.randint(2, 3)
        grid_y = random.randint(2, 3)

        spacing = random.randint(20, 35)

        index = 0
        mixed = random.choice([True, False])
        unit_type = random.choice(GFLAK)

        for i in range(grid_x):
            for j in range(grid_y):
                index = index + 1
                self.add_unit(
                    unit_type,
                    "AAA#" + str(index),
                    self.position.x + spacing * i + random.randint(1, 5),
                    self.position.y + spacing * j + random.randint(1, 5),
                    self.heading,
                )

                if mixed:
                    unit_type = random.choice(GFLAK)

        # Search lights
        search_pos = self.get_circular_position(random.randint(2, 3), 80)
        for index, pos in enumerate(search_pos):
            self.add_unit(
                AirDefence.SL_Flakscheinwerfer_37,
                "SearchLight#" + str(index),
                pos[0],
                pos[1],
                self.heading,
            )

        # Support
        self.add_unit(
            AirDefence.PU_Maschinensatz_33,
            "MC33#",
            self.position.x - 20,
            self.position.y - 20,
            self.heading,
        )
        self.add_unit(
            AirDefence.AAA_SP_Kdo_G_40,
            "KDO#",
            self.position.x - 25,
            self.position.y - 20,
            self.heading,
        )

        # Commander
        self.add_unit(
            Unarmed.Kübelwagen_82,
            "Kubel#",
            self.position.x - 35,
            self.position.y - 20,
            self.heading,
        )

        # Some Opel Blitz trucks
        for i in range(int(max(1, grid_x / 2))):
            for j in range(int(max(1, grid_x / 2))):
                self.add_unit(
                    Unarmed.Blitz_3_6_6700A,
                    "BLITZ#" + str(index),
                    self.position.x + 125 + 15 * i + random.randint(1, 5),
                    self.position.y + 15 * j + random.randint(1, 5),
                    75,
                )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
