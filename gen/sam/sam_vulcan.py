import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class VulcanGenerator(AirDefenseGroupGenerator):
    """
    This generate a Vulcan group
    """

    name = "Vulcan Group"
    price = 25

    def generate(self):
        self.add_unit(
            AirDefence.SPAAA_Vulcan_M163,
            "SPAAA",
            self.position.x,
            self.position.y,
            self.heading,
        )
        if random.randint(0, 1) == 1:
            self.add_unit(
                AirDefence.SPAAA_Vulcan_M163,
                "SPAAA2",
                self.position.x,
                self.position.y,
                self.heading,
            )
        self.add_unit(
            Unarmed.Truck_M818_6x6,
            "TRUCK",
            self.position.x + 80,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.AAA
