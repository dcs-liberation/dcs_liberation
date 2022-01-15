from dcs.mapping import Point
from dcs.vehicles import AirDefence

from game.theater.theatergroundobject import AirDefenseRange, SkynetRole
from gen.to_remove.airdefensegroupgenerator import (
    AirDefenseGroupGenerator,
)


class HawkGenerator(AirDefenseGroupGenerator):
    """
    This generate an HAWK group
    """

    name = "Hawk Site"

    def generate(self) -> None:
        self.add_unit(
            AirDefence.Hawk_sr,
            "SR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Hawk_pcp,
            "PCP",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Hawk_tr,
            "TR",
            self.position.x + 40,
            self.position.y,
            self.heading,
        )

        # Triple A for close range defense
        aa_group = self.add_auxiliary_group(SkynetRole.NoSkynetBehavior)
        self.add_unit_to_group(
            aa_group,
            AirDefence.Vulcan,
            "AAA",
            self.position + Point(20, 30),
            self.heading,
        )

        num_launchers = 6
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Hawk_ln,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
