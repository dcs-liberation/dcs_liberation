import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)
from game.utils import Heading

GFLAK = [
    AirDefence.Flak38,
    AirDefence.Flak18,
    AirDefence.Flak36,
    AirDefence.Flak37,
    AirDefence.Flak41,
    AirDefence.Flak30,
]


class FlakGenerator(AirDefenseGroupGenerator):
    """
    This generate a German flak artillery group
    """

    name = "Flak Site"

    def generate(self) -> None:
        index = 0
        mixed = random.choice([True, False])
        unit_type = random.choice(GFLAK)

        for i in range(4):
            index = index + 1
            spacing_x = random.randint(10, 40)
            spacing_y = random.randint(10, 40)
            self.add_unit(
                unit_type,
                "AAA#" + str(index),
                self.position.x + spacing_x * i + random.randint(1, 5),
                self.position.y + spacing_y * i + random.randint(1, 5),
                self.heading,
            )

            if mixed:
                unit_type = random.choice(GFLAK)

        # Search lights
        search_pos = self.get_circular_position(random.randint(2, 3), 80)
        for index, pos in enumerate(search_pos):
            self.add_unit(
                AirDefence.Flakscheinwerfer_37,
                "SearchLight#" + str(index),
                pos[0],
                pos[1],
                self.heading,
            )

        # Support
        self.add_unit(
            AirDefence.Maschinensatz_33,
            "MC33#",
            self.position.x - 20,
            self.position.y - 20,
            self.heading,
        )
        self.add_unit(
            AirDefence.KDO_Mod40,
            "KDO#",
            self.position.x - 25,
            self.position.y - 20,
            self.heading,
        )

        # Commander
        self.add_unit(
            Unarmed.Kubelwagen_82,
            "Kubel#",
            self.position.x - 35,
            self.position.y - 20,
            self.heading,
        )

        # Some Opel Blitz trucks
        for i in range(int(max(1, 2))):
            for j in range(int(max(1, 2))):
                self.add_unit(
                    Unarmed.Blitz_36_6700A,
                    "BLITZ#" + str(index),
                    self.position.x + 125 + 15 * i + random.randint(1, 5),
                    self.position.y + 15 * j + random.randint(1, 5),
                    Heading.from_degrees(75),
                )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
