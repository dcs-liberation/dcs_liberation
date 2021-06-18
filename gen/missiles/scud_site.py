import random

from dcs.vehicles import Unarmed, MissilesSS, AirDefence

from gen.sam.group_generator import GroupGenerator


class ScudGenerator(GroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(ScudGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        # Scuds
        self.add_unit(
            MissilesSS.SSM_SS_1C_Scud_B,
            "V1#0",
            self.position.x,
            self.position.y + random.randint(1, 8),
            self.heading,
        )
        self.add_unit(
            MissilesSS.SSM_SS_1C_Scud_B,
            "V1#1",
            self.position.x + 50,
            self.position.y + random.randint(1, 8),
            self.heading,
        )
        self.add_unit(
            MissilesSS.SSM_SS_1C_Scud_B,
            "V1#2",
            self.position.x + 100,
            self.position.y + random.randint(1, 8),
            self.heading,
        )

        # Commander
        self.add_unit(
            Unarmed.LUV_UAZ_469_Jeep,
            "Kubel#0",
            self.position.x - 35,
            self.position.y - 20,
            self.heading,
        )

        # Shorad
        self.add_unit(
            AirDefence.SPAAA_ZSU_23_4_Shilka_Gun_Dish,
            "SHILKA#0",
            self.position.x - 55,
            self.position.y - 38,
            self.heading,
        )

        self.add_unit(
            AirDefence.SAM_SA_9_Strela_1_Gaskin_TEL,
            "STRELA#0",
            self.position.x + 200,
            self.position.y + 15,
            90,
        )
