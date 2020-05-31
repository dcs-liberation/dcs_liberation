import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator

GFLAK = [AirDefence.AAA_Flak_Vierling_38, AirDefence.AAA_8_8cm_Flak_18, AirDefence.AAA_8_8cm_Flak_36, AirDefence.AAA_8_8cm_Flak_37, AirDefence.AAA_8_8cm_Flak_41, AirDefence.AAA_Flak_38]

class FlakGenerator(GroupGenerator):
    """
    This generate a German flak artillery group
    """

    def generate(self):
        grid_x = random.randint(2, 4)
        grid_y = random.randint(2, 4)

        spacing = random.randint(10,40)

        index = 0
        mixed = random.choice([True, False])
        unit_type = random.choice(GFLAK)

        for i in range(grid_x):
            for j in range(grid_y):
                index = index+1
                self.add_unit(unit_type, "AAA#" + str(index),
                              self.position.x + spacing*i,
                              self.position.y + spacing*j, self.heading)

                if(mixed):
                    unit_type = random.choice(GFLAK)

        # Enough Opel truck to transport the guns
        for i in range(grid_x):
            for j in range(grid_y):
                self.add_unit(Unarmed.Blitz_3_6_6700A, "AAA#" + str(index),
                              self.position.x + 200 + 9*i,
                              self.position.y + 9*j, 90)