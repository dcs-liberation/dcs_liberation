import random

from gen.sam.group_generator import GroupGenerator


class CarrierGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction):
        super(CarrierGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        # Add carrier
        if "aircraft_carrier" in self.faction.keys():
            carrier_type = random.choice(self.faction["aircraft_carrier"])
            self.add_unit(carrier_type, "Carrier", self.position.x, self.position.y, self.heading)
        else:
            return

        # Add destroyers escort
        dd_type = random.choice(self.faction["destroyer"])
        self.add_unit(dd_type, "DD1", self.position.x + 250, self.position.y + 450, self.heading)
        self.add_unit(dd_type, "DD2", self.position.x + 250, self.position.y - 450, self.heading)

        self.add_unit(dd_type, "DD3", self.position.x + 450, self.position.y + 850, self.heading)
        self.add_unit(dd_type, "DD4", self.position.x + 450, self.position.y - 850, self.heading)