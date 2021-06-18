from dcs.vehicles import MissilesSS, Unarmed, AirDefence

from gen.sam.group_generator import GroupGenerator


class SilkwormGenerator(GroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(SilkwormGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        positions = self.get_circular_position(5, launcher_distance=120, coverage=180)

        self.add_unit(
            MissilesSS.Silkworm_SR,
            "SR#0",
            self.position.x,
            self.position.y,
            self.heading,
        )

        # Launchers
        for i, p in enumerate(positions):
            self.add_unit(
                MissilesSS.Silkworm_SR,
                "Missile#" + str(i),
                p[0],
                p[1],
                self.heading,
            )

        # Commander
        self.add_unit(
            Unarmed.KAMAZ_Truck,
            "KAMAZ#0",
            self.position.x - 35,
            self.position.y - 20,
            self.heading,
        )

        # Shorad
        self.add_unit(
            AirDefence.ZSU_23_4_Shilka,
            "SHILKA#0",
            self.position.x - 55,
            self.position.y - 38,
            self.heading,
        )

        # Shorad 2
        self.add_unit(
            AirDefence.Strela_1_9P31,
            "STRELA#0",
            self.position.x + 200,
            self.position.y + 15,
            90,
        )
