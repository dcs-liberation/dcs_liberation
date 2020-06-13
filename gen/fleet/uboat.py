import random

from dcs.ships import Uboat_VIIC_U_flak

from gen.sam.group_generator import GroupGenerator


class UBoatGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction):
        super(UBoatGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        for i in range(random.randint(2, 6)):
            self.add_unit(Uboat_VIIC_U_flak, "Uboat" + str(i), self.position.x + i * random.randint(100, 250), self.position.y + (random.randint(100, 200)-100), self.heading)

        self.get_generated_group().points[0].speed = 20