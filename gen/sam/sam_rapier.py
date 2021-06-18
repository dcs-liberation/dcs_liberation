import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class RapierGenerator(AirDefenseGroupGenerator):
    """
    This generate a Rapier Group
    """

    name = "Rapier AA Site"
    price = 50

    def generate(self):
        self.add_unit(
            AirDefence.SAM_Rapier_Blindfire_TR,
            "BT",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.SAM_Rapier_Tracker,
            "OT",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

        num_launchers = random.randint(3, 6)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=80, coverage=240
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SAM_Rapier_LN,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
