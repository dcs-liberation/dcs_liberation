import random

from gen.fleet.dd_group import DDGroupGenerator
from gen.sam.group_generator import ShipGroupGenerator
from dcs.ships import *


class ChineseNavyGroupGenerator(ShipGroupGenerator):

    def generate(self):

        include_frigate = random.choice([True, True, False])
        include_dd = random.choice([True, False])

        if include_dd:
            include_cc = random.choice([True, False])
        else:
            include_cc = False

        if include_frigate:
            self.add_unit(Type_054A_Frigate, "FF1", self.position.x + 1200, self.position.y + 900, self.heading)
            self.add_unit(Type_054A_Frigate, "FF2", self.position.x + 1200, self.position.y - 900, self.heading)

        if include_dd:
            dd_type = random.choice([Type_052C_Destroyer, Type_052B_Destroyer])
            self.add_unit(dd_type, "FF1", self.position.x + 2400, self.position.y + 900, self.heading)
            self.add_unit(dd_type, "FF2", self.position.x + 2400, self.position.y - 900, self.heading)

        if include_cc:
            cc_type = random.choice([CGN_1144_2_Pyotr_Velikiy])
            self.add_unit(cc_type, "CC1", self.position.x, self.position.y, self.heading)

        self.get_generated_group().points[0].speed = 20


class Type54GroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(Type54GroupGenerator, self).__init__(game, ground_object, faction, Type_054A_Frigate)
