from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)
from pydcs_extensions.highdigitsams import highdigitsams


class SA17Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-17 group
    """

    name = "SA-17 Grizzly Battery"

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

        positions = self.get_circular_position(3, launcher_distance=140, coverage=180)

        for i, position in enumerate(positions):
            self.add_unit(
                highdigitsams.SAM_SA_17_Buk_M1_2_LN_9A310M1_2,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
