import random

from dcs.ships import Schnellboot_type_S130

from gen.sam.group_generator import GroupGenerator


class SchnellbootGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction):
        super(SchnellbootGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        for i in range(random.randint(2, 4)):
            self.add_unit(Schnellboot_type_S130, "Schnellboot" + str(i), self.position.x + i * random.randint(100, 250), self.position.y + (random.randint(100, 200)-100), self.heading)

        self.get_generated_group().points[0].speed = 20