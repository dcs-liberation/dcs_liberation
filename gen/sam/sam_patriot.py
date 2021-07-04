from dcs.mapping import Point
from dcs.vehicles import AirDefence

from game.theater.theatergroundobject import IADSRole
from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class PatriotGenerator(AirDefenseGroupGenerator):
    """
    This generate a Patriot group
    """

    name = "Patriot Battery"

    def generate(self) -> None:
        # Command Post
        self.add_unit(
            AirDefence.Patriot_str,
            "STR",
            self.position.x + 30,
            self.position.y + 30,
            self.heading,
        )
        self.add_unit(
            AirDefence.Patriot_AMG,
            "MRC",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Patriot_ECS,
            "MSQ",
            self.position.x + 30,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Patriot_cp,
            "ICC",
            self.position.x + 60,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Patriot_EPP,
            "EPP",
            self.position.x,
            self.position.y + 30,
            self.heading,
        )

        positions = self.get_circular_position(8, launcher_distance=120, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Patriot_ln,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

        # Short range protection for high value site
        aa_group = self.add_auxiliary_group(IADSRole.NoBehavior)
        positions = self.get_circular_position(2, launcher_distance=200, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(
                aa_group,
                AirDefence.Vulcan,
                f"SPAAA#{i}",
                Point(x, y),
                heading,
            )
        positions = self.get_circular_position(2, launcher_distance=300, coverage=360)
        for i, (x, y, heading) in enumerate(positions):
            self.add_unit_to_group(
                aa_group,
                AirDefence.M1097_Avenger,
                f"Avenger#{i}",
                Point(x, y),
                heading,
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Long
