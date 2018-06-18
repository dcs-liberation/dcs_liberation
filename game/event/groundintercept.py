import math
import random

from dcs.task import *

from game import *
from game.event import *
from userdata.debriefing import Debriefing


class GroundInterceptEvent(Event):
    BONUS_BASE = 3
    TARGET_AMOUNT_FACTOR = 2
    TARGET_VARIETY = 2
    STRENGTH_INFLUENCE = 0.3
    SUCCESS_TARGETS_HIT_PERCENTAGE = 0.5

    targets = None  # type: db.ArmorDict

    def __str__(self):
        return "Ground intercept from {} at {}".format(self.from_cp, self.to_cp)

    def is_successfull(self, debriefing: Debriefing):
        total_targets = sum(self.targets.values())
        destroyed_targets = 0
        for unit, count in debriefing.destroyed_units[self.defender_name].items():
            if unit in self.targets:
                destroyed_targets += count

        return (float(destroyed_targets) / float(total_targets)) >= self.SUCCESS_TARGETS_HIT_PERCENTAGE

    def commit(self, debriefing: Debriefing):
        super(GroundInterceptEvent, self).commit(debriefing)

        if self.from_cp.captured:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(+self.STRENGTH_INFLUENCE)
        else:
            assert False

    def skip(self):
        if not self.to_cp.captured:
            self.to_cp.base.affect_strength(+0.1)
        else:
            pass

    def player_attacking(self, strikegroup: db.PlaneDict, clients: db.PlaneDict):
        suitable_unittypes = db.find_unittype(PinpointStrike, self.defender_name)
        random.shuffle(suitable_unittypes)
        unittypes = suitable_unittypes[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.difficulty * self.TARGET_AMOUNT_FACTOR), 1)
        self.targets = {unittype: typecount for unittype in unittypes}

        op = GroundInterceptOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      attacker_clients=clients,
                                      defender_clients={},
                                      from_cp=self.from_cp,
                                      to_cp=self.to_cp)
        op.setup(target=self.targets,
                 strikegroup=strikegroup)

        self.operation = op


