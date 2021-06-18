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
    price = 180

    def generate(self):
        self.add_unit(
            AirDefence.SAM_SA_11_Buk_Gadfly_Snow_Drift_SR,
            "SR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.SAM_SA_11_Buk_Gadfly_C2,
            "CC",
            self.position.x,
            self.position.y,
            self.heading,
        )

        num_launchers = random.randint(2, 4)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=140, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SAM_SA_11_Buk_Gadfly_Fire_Dome_TEL,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
