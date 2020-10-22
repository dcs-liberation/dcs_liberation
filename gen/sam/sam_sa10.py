import random

from dcs.vehicles import AirDefence

from gen.sam.genericsam_group_generator import GenericSamGroupGenerator


class SA10Generator(GenericSamGroupGenerator):
    """
    This generate a SA-10 group
    """

    name = "SA-10/S-300PS Battery"
    price = 450

    def generate(self):
        # Search Radar
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_SR_5N66M, "SR1", self.position.x, self.position.y + 40, self.heading)

        # Search radar for missiles (optionnal)
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_SR_64H6E, "SR2", self.position.x - 40, self.position.y, self.heading)

        # Command Post
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_CP_54K6, "CP", self.position.x, self.position.y, self.heading)

        # 2 Tracking radars
        self.add_unit(AirDefence.SAM_SA_10_S_300PS_TR_30N6, "TR1", self.position.x - 40, self.position.y - 40, self.heading)

        self.add_unit(AirDefence.SAM_SA_10_S_300PS_TR_30N6, "TR2", self.position.x + 40, self.position.y - 40,
                      self.heading)

        # 2 different launcher type (C & D)
        num_launchers = random.randint(6, 8)
        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=360)
        for i, position in enumerate(positions):
            if i%2 == 0:
                self.add_unit(AirDefence.SAM_SA_10_S_300PS_LN_5P85C, "LN#" + str(i), position[0], position[1], position[2])
            else:
                self.add_unit(AirDefence.SAM_SA_10_S_300PS_LN_5P85D, "LN#" + str(i), position[0], position[1], position[2])

        # Then let's add short range protection to this high value site
        # Sa-13 Strela are great for that
        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=300, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_SA_13_Strela_10M3_9A35M3, "IR#" + str(i), position[0], position[1], position[2])

        # And even some AA
        num_launchers = random.randint(6, 8)
        positions = self.get_circular_position(num_launchers, launcher_distance=350, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SPAAA_ZSU_23_4_Shilka, "AA#" + str(i), position[0], position[1], position[2])
