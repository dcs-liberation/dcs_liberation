import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import GroupGenerator


class ZU23InsurgentGenerator(GroupGenerator):
    """
    This generate a ZU23 insurgent flak artillery group
    """

    name = "Zu-23 Site"
    price = 56

    def generate(self):
        grid_x = random.randint(2, 3)
        grid_y = random.randint(2, 3)

        spacing = random.randint(10,40)

        index = 0
        for i in range(grid_x):
            for j in range(grid_y):
                index = index+1
                self.add_unit(AirDefence.AAA_ZU_23_Insurgent_Closed, "AAA#" + str(index),
                              self.position.x + spacing*i,
                              self.position.y + spacing*j, self.heading)