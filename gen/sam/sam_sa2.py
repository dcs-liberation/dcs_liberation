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

    def generate(self) -> None:
        self.add_unit(
            AirDefence.P_19_s_125_sr,
            "SR",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.SNR_75V,
            "TR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

        num_launchers = 6
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.S_75M_Volhov,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
