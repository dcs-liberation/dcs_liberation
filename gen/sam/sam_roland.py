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
        self.add_unit(
            AirDefence.SAM_Roland_EWR,
            "EWR",
            self.position.x + 40,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.SAM_Roland_ADS,
            "ADS",
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
        return AirDefenseRange.Short
