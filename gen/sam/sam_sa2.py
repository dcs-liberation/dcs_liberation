import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA2Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-2 group
    """

    name = "SA-2/S-75 Site"
    price = 74

    def generate(self):
        self.add_unit(
            AirDefence.SAM_P19_Flat_Face_SR__SA_2_3, "SR", self.position.x, self.position.y, self.heading
        )
        self.add_unit(
            AirDefence.SAM_SA_2_S_75_Fan_Song_TR,
            "TR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

        num_launchers = random.randint(3, 6)
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.SAM_SA_2_S_75_Guideline_LN,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
