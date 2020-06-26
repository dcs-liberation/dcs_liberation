import random

from gen.fleet.dd_group import DDGroupGenerator
from gen.sam.group_generator import GroupGenerator
from dcs.ships import *


class RussianNavyGroupGenerator(GroupGenerator):

    def __init__(self, game, ground_object, faction):
        super(RussianNavyGroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self):

        include_frigate = random.choice([True, True, False])
        include_dd = random.choice([True, False])

        if include_dd:
            include_cc = random.choice([True, False])
        else:
            include_cc = False

        if include_frigate:
            frigate_type = random.choice([FFL_1124_4_Grisha, FSG_1241_1MP_Molniya])
            self.add_unit(frigate_type, "FF1", self.position.x + 1200, self.position.y + 900, self.heading)
            self.add_unit(frigate_type, "FF2", self.position.x + 1200, self.position.y - 900, self.heading)

        if include_dd:
            dd_type = random.choice([FFG_11540_Neustrashimy, FF_1135M_Rezky])
            self.add_unit(dd_type, "FF1", self.position.x + 2400, self.position.y + 900, self.heading)
            self.add_unit(dd_type, "FF2", self.position.x + 2400, self.position.y - 900, self.heading)

        if include_cc:
            cc_type = random.choice([CG_1164_Moskva, CGN_1144_2_Pyotr_Velikiy])
            self.add_unit(cc_type, "CC1", self.position.x, self.position.y, self.heading)

        self.get_generated_group().points[0].speed = 20


class GrishaGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(GrishaGroupGenerator, self).__init__(game, ground_object, faction, FFL_1124_4_Grisha)


class MolniyaGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(MolniyaGroupGenerator, self).__init__(game, ground_object, faction, FSG_1241_1MP_Molniya)


class KiloSubGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(KiloSubGroupGenerator, self).__init__(game, ground_object, faction, SSK_877)


class TangoSubGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object, faction):
        super(TangoSubGroupGenerator, self).__init__(game, ground_object, faction, SSK_641B)

