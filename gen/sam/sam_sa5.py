from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA5Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-5 group
    """

    name = "SA-5/S-200 Site"

    def generate(self) -> None:
        self.add_unit(
            AirDefence.RLS_19J6,
            "SR",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.RPC_5N62V,
            "TR",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

        num_launchers = 6
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=360
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.S_200_Launcher,
                "LN#" + str(i),
                position[0],
                position[1],
                position[2],
            )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Long
