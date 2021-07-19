from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA15Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-15 group
    """

    name = "SA-15 Tor Group"

    def generate(self) -> None:
        num_launchers = 2
        positions = self.get_circular_position(
            num_launchers, launcher_distance=120, coverage=360
        )
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Tor_9A331,
                "ADS#" + str(i),
                position[0],
                position[1],
                position[2],
            )
        self.add_unit(
            Unarmed.UAZ_469,
            "EWR",
            self.position.x + 40,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            Unarmed.KAMAZ_Truck,
            "TRUCK",
            self.position.x + 80,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
