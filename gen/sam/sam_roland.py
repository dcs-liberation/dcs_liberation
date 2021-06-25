from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class RolandGenerator(AirDefenseGroupGenerator):
    """
    This generate a Roland group
    """

    name = "Roland Site"
    price = 40

    def generate(self):
        num_launchers = 2
        self.add_unit(
            AirDefence.Roland_Radar,
            "EWR",
            self.position.x + 40,
            self.position.y,
            self.heading,
        )
        positions = self.get_circular_position(
            num_launchers, launcher_distance=80, coverage=240
        )

        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Roland_ADS,
                "ADS#" + str(i),
                position[0],
                position[1],
                position[2],
            )
        self.add_unit(
            Unarmed.M_818,
            "TRUCK",
            self.position.x + 80,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
