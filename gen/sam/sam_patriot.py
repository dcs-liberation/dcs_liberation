import random

from dcs.mapping import Point
from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class PatriotGenerator(AirDefenseGroupGenerator):
    """
    This generate a Patriot group
    """

    name = "Patriot Battery"
    price = 240

    def generate(self):
        # Command Post
        self.add_unit(AirDefence.SAM_Patriot_STR_AN_MPQ_53, "STR", self.position.x + 30, self.position.y + 30, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_AMG_AN_MRC_137, "MRC", self.position.x, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_ECS_AN_MSQ_104, "MSQ", self.position.x + 30, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_ICC, "ICC", self.position.x + 60, self.position.y, self.heading)
        self.add_unit(AirDefence.SAM_Patriot_EPP_III, "EPP", self.position.x, self.position.y + 30, self.heading)

        num_launchers = random.randint(3, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=120, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(AirDefence.SAM_Patriot_LN_M901, "LN#" + str(i), position[0], position[1], position[2])

        # Short range protection for high value site
        aa_group = self.add_auxiliary_group("AA")
        num_launchers = random.randint(3, 4)
        positions = self.get_circular_position(num_launchers, launcher_distance=200, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(aa_group, AirDefence.AAA_Vulcan_M163,
                                   f"SPAAA#{i}", Point(x, y), heading)

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Long
