from dcs.vehicles import AirDefence

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class SA8Generator(AirDefenseGroupGenerator):
    """
    This generate a SA-8 group
    """

    name = "SA-8 OSA Site"
    price = 55

    def generate(self):
        self.add_unit(
            AirDefence.SAM_SA_8_Osa_9A33,
            "OSA",
            self.position.x,
            self.position.y,
            self.heading,
        )
        self.add_unit(
            AirDefence.SAM_SA_8_Osa_LD_9T217,
            "LD",
            self.position.x + 20,
            self.position.y,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Medium
