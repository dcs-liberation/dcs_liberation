import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
    SkynetRole,
)


class RapierGenerator(AirDefenseGroupGenerator):
    """
    This generate a Rapier Group
    """

    name = "Rapier AA Site"
    price = 50

    def generate(self):
        self.add_unit(
            AirDefence.Rapier_fsa_blindfire_radar,
            "BT",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Rapier_fsa_optical_tracker_unit,
            "OT",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=80, coverage=240
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Rapier_fsa_launcher,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short

    @classmethod
    def primary_group_role(cls) -> SkynetRole:
        return SkynetRole.Sam
