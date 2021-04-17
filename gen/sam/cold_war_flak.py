import random

from dcs.vehicles import AirDefence, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)
from gen.sam.group_generator import GroupGenerator


class EarlyColdWarFlakGenerator(AirDefenseGroupGenerator):
    """
    This generator attempt to mimic an early cold-war era flak AAA site.
    The Flak 18 88mm is used as the main long range gun and 2 Bofors 40mm guns provide short range protection.

    This does not include search lights and telemeter computer (Kdo.G 40) because these are paid units only available in WW2 asset pack
    """

    name = "Early Cold War Flak Site"
    price = 58

    def generate(self):

        spacing = random.randint(30, 60)
        index = 0

        # Long range guns
        for i in range(3):
            for j in range(2):
                index = index + 1
                self.add_unit(
                    AirDefence.AAA_8_8cm_Flak_18,
                    "AAA#" + str(index),
                    self.position.x + spacing * i + random.randint(1, 5),
                    self.position.y + spacing * j + random.randint(1, 5),
                    self.heading,
                )

        # Short range guns
        self.add_unit(
            AirDefence.AAA_40mm_Bofors,
            "SHO#1",
            self.position.x - 40,
            self.position.y - 40,
            self.heading + 180,
        ),
        self.add_unit(
            AirDefence.AAA_40mm_Bofors,
            "SHO#2",
            self.position.x + spacing * 2 + 40,
            self.position.y + spacing + 40,
            self.heading,
        ),

        # Add a truck
        self.add_unit(
            Unarmed.Truck_KAMAZ_43101,
            "Truck#",
            self.position.x - 60,
            self.position.y - 20,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short


class ColdWarFlakGenerator(AirDefenseGroupGenerator):
    """
    This generator attempt to mimic a cold-war era flak AAA site.
    The Flak 18 88mm is used as the main long range gun while 2 Zu-23 guns provide short range protection.
    The site is also fitted with a P-19 radar for early detection.
    """

    name = "Cold War Flak Site"
    price = 72

    def generate(self):

        spacing = random.randint(30, 60)
        index = 0

        # Long range guns
        for i in range(3):
            for j in range(2):
                index = index + 1
                self.add_unit(
                    AirDefence.AAA_8_8cm_Flak_18,
                    "AAA#" + str(index),
                    self.position.x + spacing * i + random.randint(1, 5),
                    self.position.y + spacing * j + random.randint(1, 5),
                    self.heading,
                )

        # Short range guns
        self.add_unit(
            AirDefence.AAA_ZU_23_Closed_Emplacement,
            "SHO#1",
            self.position.x - 40,
            self.position.y - 40,
            self.heading + 180,
        ),
        self.add_unit(
            AirDefence.AAA_ZU_23_Closed_Emplacement,
            "SHO#2",
            self.position.x + spacing * 2 + 40,
            self.position.y + spacing + 40,
            self.heading,
        ),

        # Add a P19 Radar for EWR
        self.add_unit(
            AirDefence.SAM_P19_Flat_Face_SR__SA_2_3,
            "SR#0",
            self.position.x - 60,
            self.position.y - 20,
            self.heading,
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
