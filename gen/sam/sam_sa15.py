from dcs.vehicles import AirDefence, Unarmed

from gen.sam.group_generator import GroupGenerator


class SA15Generator(GroupGenerator):
    """
    This generate a SA-15 group
    """

    name = "SA-15 Tor Group"

    def generate(self):
        self.add_unit(AirDefence.SAM_SA_15_Tor_9A331, "ADS", self.position.x, self.position.y, self.heading)
        self.add_unit(Unarmed.Transport_UAZ_469, "EWR", self.position.x + 40, self.position.y, self.heading)
        self.add_unit(Unarmed.Transport_KAMAZ_43101, "TRUCK", self.position.x + 80, self.position.y, self.heading)