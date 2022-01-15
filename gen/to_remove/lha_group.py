import random

from dcs import Point

from gen.group_generator import ShipGroupGenerator


class LHAGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:

        # Add carrier
        if len(self.faction.helicopter_carrier) > 0:
            carrier_type = random.choice(self.faction.helicopter_carrier)
            self.add_unit(
                carrier_type, "LHA", self.position.x, self.position.y, self.heading
            )

        # Add destroyers escort
        aux_group = self.add_auxiliary_group()
        if len(self.faction.destroyers) > 0:
            dd_type = random.choice(self.faction.destroyers)
            self.add_unit_to_group(
                aux_group,
                dd_type,
                "DD1",
                Point(self.position.x + 1250, self.position.y + 1450),
                self.heading,
            )
            self.add_unit_to_group(
                aux_group,
                dd_type,
                "DD2",
                Point(self.position.x + 1250, self.position.y - 1450),
                self.heading,
            )

        self.get_generated_group().points[0].speed = 20
