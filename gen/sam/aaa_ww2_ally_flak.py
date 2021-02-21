import random

from dcs.vehicles import AirDefence, Armor, Unarmed

from gen.sam.airdefensegroupgenerator import (
    AirDefenseRange,
    AirDefenseGroupGenerator,
)


class AllyWW2FlakGenerator(AirDefenseGroupGenerator):
    """
    This generate an ally flak artillery group
    """

    name = "WW2 Ally Flak Site"
    price = 140

    def generate(self):

        positions = self.get_circular_position(4, launcher_distance=30, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.AA_gun_QF_3_7,
                "AA#" + str(i),
                position[0],
                position[1],
                position[2],
            )

        positions = self.get_circular_position(8, launcher_distance=60, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.AAA_M1_37mm,
                "AA#" + str(4 + i),
                position[0],
                position[1],
                position[2],
            )

        positions = self.get_circular_position(8, launcher_distance=90, coverage=360)
        for i, position in enumerate(positions):
            self.add_unit(
                AirDefence.AAA_M45_Quadmount,
                "AA#" + str(12 + i),
                position[0],
                position[1],
                position[2],
            )

        # Add a commander truck
        self.add_unit(
            Unarmed.Willys_MB,
            "CMD#1",
            self.position.x,
            self.position.y - 20,
            random.randint(0, 360),
        )
        self.add_unit(
            Armor.M30_Cargo_Carrier,
            "LOG#1",
            self.position.x,
            self.position.y + 20,
            random.randint(0, 360),
        )
        self.add_unit(
            Armor.M4_Tractor,
            "LOG#2",
            self.position.x + 20,
            self.position.y,
            random.randint(0, 360),
        )
        self.add_unit(
            Unarmed.Bedford_MWD,
            "LOG#3",
            self.position.x - 20,
            self.position.y,
            random.randint(0, 360),
        )

    @classmethod
    def range(cls) -> AirDefenseRange:
        return AirDefenseRange.Short
