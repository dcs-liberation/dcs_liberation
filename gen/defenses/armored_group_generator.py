import random

from gen.sam.group_generator import GroupGenerator


class ArmoredGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, unit_type):
        super(ArmoredGroupGenerator, self).__init__(game, ground_object)
        self.unit_type = unit_type

    def generate(self):

        grid_x = random.randint(2, 3)
        grid_y = random.randint(1, 2)

        spacing = random.randint(30, 80)

        index = 0
        for i in range(grid_x):
            for j in range(grid_y):
                index = index + 1
                self.add_unit(self.unit_type, "Armor#" + str(index),
                              self.position.x + spacing * i,
                              self.position.y + spacing * j, self.heading)


class FixedSizeArmorGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, unit_type, size):
        super(FixedSizeArmorGroupGenerator, self).__init__(game, ground_object)
        self.unit_type = unit_type
        self.size = size

    def generate(self):
        spacing = random.randint(20, 70)

        index = 0
        for i in range(self.size):
            index = index + 1
            self.add_unit(self.unit_type, "Armor#" + str(index),
                            self.position.x + spacing * i,
                            self.position.y, self.heading)

