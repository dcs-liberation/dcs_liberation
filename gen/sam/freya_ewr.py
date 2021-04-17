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
            AirDefence.EWR_FuMG_401_Freya_LZ,
            "EWR#1",
            self.position.x,
            self.position.y,
            self.heading,
        )

        positions = self.get_circular_position(4, launcher_distance=50, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.AAA_Flak_Vierling_38_Quad_20mm,
                "AA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

        positions = self.get_circular_position(4, launcher_distance=100, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.AAA_8_8cm_Flak_18,
                "AA#" + str(4 + i),
                position[0],
                position[1],
                position[2],
            )

        # Command/Logi
        self.add_unit(
            Unarmed.LUV_Kubelwagen_82,
            "Kubel#1",
            self.position.x - 20,
            self.position.y - 20,
            self.heading,
        )
        self.add_unit(
            Unarmed.Carrier_Sd_Kfz_7_Tractor,
            "Sdkfz#1",
            self.position.x + 20,
            self.position.y + 22,
            self.heading,
        )
        self.add_unit(
            Unarmed.LUV_Kettenrad,
            "Sdkfz#2",
            self.position.x - 22,
            self.position.y + 20,
            self.heading,
        )

        # PU_Maschinensatz_33 and Kdo.g 40 Telemeter
        self.add_unit(
            AirDefence.PU_Maschinensatz_33,
            "Energy#1",
            self.position.x + 20,
            self.position.y - 20,
            self.heading,
        )
        self.add_unit(
            AirDefence.AAA_SP_Kdo_G_40,
            "Telemeter#1",
            self.position.x + 20,
            self.position.y - 10,
            self.heading,
        )
        self.add_unit(
            Infantry.Infantry_Mauser_98,
            "Inf#1",
            self.position.x + 20,
            self.position.y - 14,
            self.heading,
        )
        self.add_unit(
            Infantry.Infantry_Mauser_98,
            "Inf#2",
            self.position.x + 20,
            self.position.y - 22,
            self.heading,
        )
        self.add_unit(
            Infantry.Infantry_Mauser_98,
            "Inf#3",
            self.position.x + 20,
            self.position.y - 24,
            self.heading + 45,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
