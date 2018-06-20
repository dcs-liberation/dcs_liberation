import math
import random

from dcs.task import *

from game import db
from game.operation.capture import CaptureOperation
from userdata.debriefing import Debriefing

from .event import Event


class CaptureEvent(Event):
    silent = True
    BONUS_BASE = 7
    STRENGTH_RECOVERY = 0.35

    def __str__(self):
        return "Attack from {} to {}".format(self.from_cp, self.to_cp)

    @property
    def threat_description(self):
        descr = "{} aircraft + CAS, {} vehicles".format(
            self.enemy_cp.base.scramble_count(),
            self.enemy_cp.base.assemble_count()
        )

        if self.is_player_attacking:
            descr += ", {} AA".format(self.enemy_cp.base.assemble_aa_count())

        return descr

    def is_successfull(self, debriefing: Debriefing):
        alive_attackers = sum([v for k, v in debriefing.alive_units[self.attacker_name].items() if db.unit_task(k) == PinpointStrike])
        alive_defenders = sum([v for k, v in debriefing.alive_units[self.defender_name].items() if db.unit_task(k) == PinpointStrike])
        attackers_success = alive_attackers > alive_defenders
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def commit(self, debriefing: Debriefing):
        super(CaptureEvent, self).commit(debriefing)
        if self.is_successfull(debriefing):
            if self.from_cp.captured:
                self.to_cp.captured = True
                self.to_cp.base.filter_units(db.UNIT_BY_COUNTRY[self.attacker_name])

            self.to_cp.base.affect_strength(+self.STRENGTH_RECOVERY)
        else:
            if not self.from_cp.captured:
                self.to_cp.captured = False
            self.to_cp.base.affect_strength(+self.STRENGTH_RECOVERY)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.captured = False

    def player_defending(self, interceptors: db.PlaneDict, clients: db.PlaneDict):
        cas = self.from_cp.base.scramble_cas()
        escort = self.from_cp.base.scramble_sweep()
        attackers = self.from_cp.base.assemble_cap()

        op = CaptureOperation(game=self.game,
                              attacker_name=self.attacker_name,
                              defender_name=self.defender_name,
                              attacker_clients={},
                              defender_clients=clients,
                              from_cp=self.from_cp,
                              to_cp=self.to_cp)

        op.setup(cas=cas,
                 escort=escort,
                 attack=attackers,
                 intercept=interceptors,
                 defense=self.to_cp.base.armor,
                 aa=self.to_cp.base.aa)

        self.operation = op

    def player_attacking(self, cas: db.PlaneDict, escort: db.PlaneDict, armor: db.ArmorDict, clients: db.PlaneDict):
        # TODO: also include CAS planes
        interceptors = self.to_cp.base.scramble_sweep()

        op = CaptureOperation(game=self.game,
                              attacker_name=self.attacker_name,
                              defender_name=self.defender_name,
                              attacker_clients=clients,
                              defender_clients={},
                              from_cp=self.from_cp,
                              to_cp=self.to_cp)

        op.setup(cas=cas,
                 escort=escort,
                 attack=armor,
                 intercept=interceptors,
                 # TODO: should strength affect this?
                 defense=self.to_cp.base.armor,
                 aa=self.to_cp.base.assemble_aa())

        self.operation = op

