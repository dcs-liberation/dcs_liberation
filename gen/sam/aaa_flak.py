import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator

GFLAK = [AirDefence.AAA_Flak_Vierling_38, AirDefence.AAA_8_8cm_Flak_18, AirDefence.AAA_8_8cm_Flak_36, AirDefence.AAA_8_8cm_Flak_37, AirDefence.AAA_8_8cm_Flak_41, AirDefence.AAA_Flak_38]

class FlakGenerator(GroupGenerator):
    """
    This generate a German flak artillery group
    """

    name = "Flak Site"

    def generate(self):
        grid_x = random.randint(2, 4)
        grid_y = random.randint(2, 4)

        spacing = random.randint(30,60)

        index = 0
        mixed = random.choice([True, False])
        unit_type = random.choice(GFLAK)

        for i in range(grid_x):
            for j in range(grid_y):
                index = index+1
                self.add_unit(unit_type, "AAA#" + str(index),
                              self.position.x + spacing*i + random.randint(1,5),
                              self.position.y + spacing*j + random.randint(1,5), self.heading)

                if(mixed):
                    unit_type = random.choice(GFLAK)

        # Search lights
        search_pos = self.get_circular_position(random.randint(2,5), 90)
        for index, pos in enumerate(search_pos):
            self.add_unit(AirDefence.Flak_Searchlight_37, "SearchLight#" + str(index), pos[0], pos[1], self.heading)

        # Support
        self.add_unit(AirDefence.Maschinensatz_33, "MC33#", self.position.x-20, self.position.y-20, self.heading)
        self.add_unit(AirDefence.AAA_Kdo_G_40, "KDO#", self.position.x - 25, self.position.y - 20,
                      self.heading)

        # Commander
        self.add_unit(Unarmed.Kübelwagen_82, "Kubel#", self.position.x - 35, self.position.y - 20,
                      self.heading)

        # Some Opel Blitz trucks
        for i in range(int(max(1,grid_x/2))):
            for j in range(int(max(1,grid_x/2))):
                self.add_unit(Unarmed.Blitz_3_6_6700A, "AAA#" + str(index),
                              self.position.x + 200 + 15*i + random.randint(1,5),
                              self.position.y + 15*j + random.randint(1,5), 90)