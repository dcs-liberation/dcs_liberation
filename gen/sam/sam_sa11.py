import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA11Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-11 group
    """

    name = "SA-11 Buk Battery"

    def generate(self) -> None:
        self.add_unit(
            AirDefence.SA_11_Buk_SR_9S18M1,
            "SR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.SA_11_Buk_CC_9S470M1,
            "CC",
            self.position.x,
            self.position.y,
            self.heading,
        )

        num_launchers = 4
        positions = self.get_circular_position(
            num_launchers, launcher_distance=140, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SA_11_Buk_LN_9A310M1,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
