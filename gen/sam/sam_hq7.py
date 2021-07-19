import random

from dcs.mapping import Point
from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
    SkynetRole,
)


class HQ7Generator(AirDefenseGroupGenerator):
    """
    This generate an HQ7 group
    """

    name = "HQ-7 Site"

    def generate(self) -> None:
        self.add_unit(
            AirDefence.HQ_7_STR_SP,
            "STR",
            self.position.x,
            self.position.y,
            self.heading,
        )

        # Triple A for close range defense
        aa_group = self.add_auxiliary_group(SkynetRole.NoSkynetBehavior)
        self.add_unit_to_group(
            aa_group,
            AirDefence.Ural_375_ZU_23,
            "AAA1",
            self.position + Point(20, 30),
            self.heading,
        )
        self.add_unit_to_group(
            aa_group,
            AirDefence.Ural_375_ZU_23,
            "AAA2",
            self.position - Point(20, 30),
            self.heading,
        )

        num_launchers = 2
        if num_launchers > 0:
            positions = self.get_circular_position(
                num_launchers, launcher_distance=120, coverage=360
            )
            for i, position in enumerate(positions):
                self.add_unit(
                    AirDefence.HQ_7_LN_SP,
                    "LN#" + str(i),
                    position[0],
                    position[1],
                    position[2],
                )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
