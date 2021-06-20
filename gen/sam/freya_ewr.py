from dcs.vehicles import AirDefence, Infantry, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class FreyaGenerator(AirDefenseGroupGenerator):
    """
    This generate a German flak artillery group using only free units, thus not requiring the WW2 asset pack
    """

    name = "Freya EWR Site"
    price = 60

    def generate(self):

        # TODO : would be better with the Concrete structure that is supposed to protect it
        self.add_unit(
            AirDefence.FuMG_401,
            "EWR#1",
            self.position.x,
            self.position.y,
            self.heading,
        )

        positions = self.get_circular_position(4, launcher_distance=50, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Flak38,
                "AA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

        positions = self.get_circular_position(4, launcher_distance=100, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.Flak18,
                "AA#" + str(4 + i),
                position[0],
                position[1],
                position[2],
            )

        # Command/Logi
        self.add_unit(
            Unarmed.Kubelwagen_82,
            "Kubel#1",
            self.position.x - 20,
            self.position.y - 20,
            self.heading,
        )
        self.add_unit(
            Unarmed.Sd_Kfz_7,
            "Sdkfz#1",
            self.position.x + 20,
            self.position.y + 22,
            self.heading,
        )
        self.add_unit(
            Unarmed.Sd_Kfz_2,
            "Sdkfz#2",
            self.position.x - 22,
            self.position.y + 20,
            self.heading,
        )

        # Maschinensatz_33 and Kdo.g 40 Telemeter
        self.add_unit(
            AirDefence.Maschinensatz_33,
            "Energy#1",
            self.position.x + 20,
            self.position.y - 20,
            self.heading,
        )
        self.add_unit(
            AirDefence.KDO_Mod40,
            "Telemeter#1",
            self.position.x + 20,
            self.position.y - 10,
            self.heading,
        )
        self.add_unit(
            Infantry.Soldier_mauser98,
            "Inf#1",
            self.position.x + 20,
            self.position.y - 14,
            self.heading,
        )
        self.add_unit(
            Infantry.Soldier_mauser98,
            "Inf#2",
            self.position.x + 20,
            self.position.y - 22,
            self.heading,
        )
        self.add_unit(
            Infantry.Soldier_mauser98,
            "Inf#3",
            self.position.x + 20,
            self.position.y - 24,
            self.heading + 45,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
