import random

from dcs.ships import LS_Samuel_Chase, LST_Mk_II

from gen.sam.group_generator import GroupGenerator


class WW2LSTGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction):
        super(WW2LSTGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        # Add LS Samuel Chase
        self.add_unit(LS_Samuel_Chase, "SamuelChase", self.position.x, self.position.y, self.heading)

        for i in range(random.randint(2, 4)):
            self.add_unit(LST_Mk_II, "LST" + str(i), self.position.x + i * random.randint(400, 600), self.position.y, self.heading)

        self.get_generated_group().points[0].speed = 20