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
    price = 55

    def generate(self):
        self.add_unit(
            AirDefence.Tor_9A331,
            "ADS",
            self.position.x,
            self.position.y,
            self.heading,
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
