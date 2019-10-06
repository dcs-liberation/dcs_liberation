import random

from dcs.vehicles import AirDefence

from gen.sam.group_generator import AntiAirGroupGenerator


class PatriotGenerator(AntiAirGroupGenerator):
    """
    This generate a Patriot group
    """

    def generate(self):
        # Command Post
        self.add_unit(AirDefence.SAM_Patriot_AMG_AN_MRC_137, "MRC", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_ECS_AN_MSQ_104, "MSQ", self.position.x + 30, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_ICC, "ICC", self.position.x + 60, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_EPP_III, "EPP", self.position.x, self.position.y + 30, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_STR_AN_MPQ_53, "ICC", self.position.x + 30, self.position.y + 30, self.heading)

        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_Patriot_LN_M901, "LN#" + str(i), position[0], position[1], position[2])

        # Short range protection for high value site
        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=300, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.AAA_Vulcan_M163, "SPAAA#" + str(i), position[0], position[1], position[2])
