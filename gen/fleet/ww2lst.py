import random

from dcs.ships import LS_Samuel_Chase, LST_Mk_II

from gen.sam.group_generator import ShipGroupGenerator


class WW2LSTGroupGenerator(ShipGroupGenerator):
    def generate(self):

        # Add LS Samuel Chase
        self.add_unit(
            LS_Samuel_Chase,
            "SamuelChase",
            self.position.x,
            self.position.y,
            self.heading,
        )

        for i in range(1, random.randint(3, 4)):
            self.add_unit(
                LST_Mk_II,
                "LST" + str(i),
                self.position.x + i * random.randint(800, 1200),
                self.position.y,
                self.heading,
            )

        self.get_generated_group().points[0].speed = 20
