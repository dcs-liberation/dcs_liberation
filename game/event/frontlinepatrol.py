import math
import random

from dcs.task import *
from dcs.vehicles import AirDefence

from game import *
from game.event import *
from game.operation.frontlinepatrol import FrontlinePatrolOperation
from userdata.debriefing import Debriefing


class FrontlinePatrolEvent(Event):
    ESCORT_FACTOR = 0.5
    STRENGTH_INFLUENCE = 0.2
    SUCCESS_FACTOR = 0.8

    cas = None  # type: db.PlaneDict
    escort = None  # type: db.PlaneDict

    @property
    def threat_description(self):
        return "{} aircraft + ? CAS".format(self.to_cp.base.scramble_count(self.game.settings.multiplier * self.ESCORT_FACTOR, CAP))

    def __str__(self):
        return "Frontline CAP"

    """
    def is_successfull(self, debriefing: Debriefing):
        total_targets = sum(self.cas.values())
        destroyed_targets = 0
        for unit, count in debriefing.destroyed_units[self.defender_name].items():
            if unit in self.cas:
                destroyed_targets += count

        if self.from_cp.captured:
            return float(destroyed_targets) / total_targets >= self.SUCCESS_TARGETS_HIT_PERCENTAGE
        else:
            return float(destroyed_targets) / total_targets < self.SUCCESS_TARGETS_HIT_PERCENTAGE
    """

    def is_successfull(self, debriefing: Debriefing):
        alive_attackers = sum([v for k, v in debriefing.alive_units[self.attacker_name].items() if db.unit_task(k) == PinpointStrike])
        alive_defenders = sum([v for k, v in debriefing.alive_units[self.defender_name].items() if db.unit_task(k) == PinpointStrike])
        attackers_success = (float(alive_attackers) / alive_defenders + 0.01) >= self.SUCCESS_FACTOR
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def commit(self, debriefing: Debriefing):
        super(FrontlinePatrolEvent, self).commit(debriefing)

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
        pass

    def player_attacking(self, interceptors: db.PlaneDict, clients: db.PlaneDict, armor: db.ArmorDict):
        self.cas = self.to_cp.base.scramble_cas(self.game.settings.multiplier)
        self.escort = self.to_cp.base.scramble_sweep(self.game.settings.multiplier * self.ESCORT_FACTOR)

        op = FrontlinePatrolOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      attacker_clients=clients,
                                      defender_clients={},
                                      from_cp=self.from_cp,
                                      to_cp=self.to_cp)

        defenders = self.to_cp.base.assemble_attack()
        op.setup(cas=self.cas,
                 escort=self.escort,
                 interceptors=interceptors,
                 armor_attackers=db.unitdict_restrict_count(armor, sum(defenders.values())),
                 armor_defenders=defenders)

        self.operation = op
