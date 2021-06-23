import random

from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA3Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-3 group
    """

    name = "SA-3/S-125 Site"
    price = 80

    def generate(self):
        self.add_unit(
            AirDefence.P_19_s_125_sr,
            "SR",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.Snr_s_125_tr,
            "TR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

        num_launchers = 4
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=180
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence._5p73_s_125_ln,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
