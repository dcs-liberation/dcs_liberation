import random

from gen.sam.group_generator import GroupGenerator


class HelicopterCarrierGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction):
        super(HelicopterCarrierGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        # Add carrier
        if self.faction["aircraft_carrier"]:
            carrier_type = random.choice(self.faction["helicopter_carrier"])
            self.add_unit(carrier_type, "Carrier", self.position.x, self.position.y, self.heading)

        # Add destroyers escort
        dd_type = random.choice(self.faction["destroyer"])
        self.add_unit(dd_type, "DD1", self.position.x + 50, self.position.y + 150, self.heading)
        self.add_unit(dd_type, "DD2", self.position.x + 50, self.position.y - 150, self.heading)

        self.add_unit(dd_type, "DD3", self.position.x + 150, self.position.y + 250, self.heading)
        self.add_unit(dd_type, "DD4", self.position.x + 150, self.position.y - 250, self.heading)