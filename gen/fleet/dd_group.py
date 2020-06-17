import random

from gen.sam.group_generator import GroupGenerator
from dcs.ships import *


class DDGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction, ddtype):
        super(DDGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction
        self.ddtype = ddtype

    def generate(self):
        self.add_unit(self.ddtype, "DD1", self.position.x + 500, self.position.y + 900, self.heading)
        self.add_unit(self.ddtype, "DD2", self.position.x + 500, self.position.y - 900, self.heading)
        self.get_generated_group().points[0].speed = 20


class OliverHazardPerryGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(OliverHazardPerryGroupGenerator, self).__init__(game, ground_object, faction, Oliver_Hazzard_Perry_class)


class ArleighBurkeGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(ArleighBurkeGroupGenerator, self).__init__(game, ground_object, faction, USS_Arleigh_Burke_IIa)
