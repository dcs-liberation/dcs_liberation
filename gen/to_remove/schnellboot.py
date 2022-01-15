import random

from dcs.ships import Schnellboot_type_S130

from gen.group_generator import ShipGroupGenerator


class SchnellbootGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:

        for i in range(random.randint(2, 4)):
            self.add_unit(
                Schnellboot_type_S130,
                "Schnellboot" + str(i),
                self.position.x + i * random.randint(100, 250),
                self.position.y + (random.randint(100, 200) - 100),
                self.heading,
            )

        self.get_generated_group().points[0].speed = 20
