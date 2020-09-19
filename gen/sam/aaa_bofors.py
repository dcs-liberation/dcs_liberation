import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class BoforsGenerator(GroupGenerator):
    """
    This generate a Bofors flak artillery group
    """

    name = "Bofors AAA"

    def generate(self):
        grid_x = random.randint(2, 4)
        grid_y = random.randint(2, 4)

        spacing = random.randint(10,40)

        index = 0
        for i in range(grid_x):
            for j in range(grid_y):
                index = index+1
                self.add_unit(AirDefence.AAA_Bofors_40mm, "AAA#" + str(index),
                              self.position.x + spacing*i,
                              self.position.y + spacing*j, self.heading)