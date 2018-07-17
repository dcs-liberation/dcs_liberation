import math
import random

from dcs.task import *
from dcs.vehicles import AirDefence

from game import *
from game.event import *
from game.operation.frontlineattack import FrontlineAttackOperation
from userdata.debriefing import Debriefing


class FrontlineAttackEvent(Event):
    TARGET_VARIETY = 2
    TARGET_AMOUNT_FACTOR = 0.5
    ATTACKER_AMOUNT_FACTOR = 0.4
    ATTACKER_DEFENDER_FACTOR = 0.7
    STRENGTH_INFLUENCE = 0.2
    SUCCESS_TARGETS_HIT_PERCENTAGE = 0.25

    defenders = None  # type: db.ArmorDict

    @property
    def threat_description(self):
        return "{} vehicles".format(self.to_cp.base.assemble_count())

    def __str__(self):
        return "Frontline attack from {} at {}".format(self.from_cp, self.to_cp)

    def is_successfull(self, debriefing: Debriefing):
        total_targets = sum(self.defenders.values())
        destroyed_targets = 0
        for unit, count in debriefing.destroyed_units[self.defender_name].items():
            if unit in self.defenders:
                destroyed_targets += count

        if self.from_cp.captured:
            return float(destroyed_targets) / total_targets >= self.SUCCESS_TARGETS_HIT_PERCENTAGE
        else:
            return float(destroyed_targets) / total_targets < self.SUCCESS_TARGETS_HIT_PERCENTAGE

    def commit(self, debriefing: Debriefing):
        super(FrontlineAttackEvent, self).commit(debriefing)

        if self.from_cp.captured:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(+self.STRENGTH_INFLUENCE)
        else:
            if self.is_successfull(debriefing):
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-0.1)

    def player_attacking(self, armor: db.ArmorDict, strikegroup: db.PlaneDict, clients: db.PlaneDict):
        self.defenders = self.to_cp.base.assemble_attack()

        op = FrontlineAttackOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      attacker_clients=clients,
                                      defender_clients={},
                                      from_cp=self.from_cp,
                                      to_cp=self.to_cp)

        op.setup(target=self.defenders,
                 attackers=db.unitdict_restrict_count(armor, sum(self.defenders.values())),
                 strikegroup=strikegroup)

        self.operation = op

