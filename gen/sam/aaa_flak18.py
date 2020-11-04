import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator


class Flak18Generator(GroupGenerator):
    """
    This generate a German flak artillery group using only free units, thus not requiring the WW2 asset pack
    """

    name = "WW2 Flak Site"
    price = 40

    def generate(self):

        spacing = random.randint(30, 60)
        index = 0

        for i in range(3):
            for j in range(2):
                index = index + 1
                self.add_unit(AirDefence.AAA_8_8cm_Flak_18, "AAA#" + str(index),
                              self.position.x + spacing * i + random.randint(1, 5),
                              self.position.y + spacing * j + random.randint(1, 5), self.heading)

        # Add a commander truck
        self.add_unit(Unarmed.Blitz_3_6_6700A, "Blitz#", self.position.x - 35, self.position.y - 20, self.heading)
