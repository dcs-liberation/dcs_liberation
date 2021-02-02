import random

from gen.sam.group_generator import ShipGroupGenerator


class CarrierGroupGenerator(ShipGroupGenerator):

    def generate(self):

        # Add carrier
        if len(self.faction.aircraft_carrier) > 0:
            carrier_type = random.choice(self.faction.aircraft_carrier)
            self.add_unit(carrier_type, "Carrier", self.position.x, self.position.y, self.heading)
        else:
            return

        # Add destroyers escort
        if len(self.faction.destroyers) > 0:
            dd_type = random.choice(self.faction.destroyers)
            self.add_unit(dd_type, "DD1", self.position.x + 2500, self.position.y + 4500, self.heading)
            self.add_unit(dd_type, "DD2", self.position.x + 2500, self.position.y - 4500, self.heading)

            self.add_unit(dd_type, "DD3", self.position.x + 4500, self.position.y + 8500, self.heading)
            self.add_unit(dd_type, "DD4", self.position.x + 4500, self.position.y - 8500, self.heading)

        self.get_generated_group().points[0].speed = 20
