import math
import random

from dcs.task import *
from dcs.vehicles import AirDefence

from game import *
from game.event import *
from game.operation.frontlinecas import FrontlineCASOperation
from userdata.debriefing import Debriefing


class FrontlineCASEvent(Event):
    TARGET_VARIETY = 2
    TARGET_AMOUNT_FACTOR = 0.5
    ATTACKER_AMOUNT_FACTOR = 0.4
    STRENGTH_INFLUENCE = 0.3
    SUCCESS_MIN_TARGETS = 3

    targets = None  # type: db.ArmorDict

    @property
    def threat_description(self):
        if not self.game.is_player_attack(self):
            return "{} aicraft".format(self.from_cp.base.scramble_count(self.game.settings.multiplier, CAS))
        else:
            return super(FrontlineCASEvent, self).threat_description

    def __str__(self):
        return "Frontline CAS from {} at {}".format(self.from_cp, self.to_cp)

    def is_successfull(self, debriefing: Debriefing):
        total_targets = sum(self.targets.values())
        destroyed_targets = 0
        for unit, count in debriefing.destroyed_units[self.defender_name].items():
            if unit in self.targets:
                destroyed_targets += count

        if self.from_cp.captured:
            return float(destroyed_targets) >= min(self.SUCCESS_MIN_TARGETS, total_targets)
        else:
            return float(destroyed_targets) < min(self.SUCCESS_MIN_TARGETS, total_targets)

    def commit(self, debriefing: Debriefing):
        super(FrontlineCASEvent, self).commit(debriefing)

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

    def player_attacking(self, strikegroup: db.PlaneDict, clients: db.PlaneDict):
        suitable_armor_targets = db.find_unittype(PinpointStrike, self.defender_name)
        random.shuffle(suitable_armor_targets)

        target_types = suitable_armor_targets[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.to_cp.base.assemble_count() * self.TARGET_AMOUNT_FACTOR), 1)
        self.targets = {unittype: typecount for unittype in target_types}

        defense_aa_unit = random.choice(self.game.commision_unit_types(self.to_cp, AirDefence))
        self.targets[defense_aa_unit] = 1

        suitable_armor_attackers = db.find_unittype(PinpointStrike, self.attacker_name)
        random.shuffle(suitable_armor_attackers)
        attacker_types = suitable_armor_attackers[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.from_cp.base.assemble_count() * self.ATTACKER_AMOUNT_FACTOR), 1)
        attackers = {unittype: typecount for unittype in attacker_types}

        op = FrontlineCASOperation(game=self.game,
                                   attacker_name=self.attacker_name,
                                   defender_name=self.defender_name,
                                   attacker_clients=clients,
                                   defender_clients={},
                                   from_cp=self.from_cp,
                                   to_cp=self.to_cp)
        op.setup(target=self.targets,
                 attackers=attackers,
                 strikegroup=strikegroup)

        self.operation = op

