import typing
import math
import random

from dcs.task import *
from dcs.vehicles import *

from game import db
from game.operation.navalintercept import NavalInterceptionOperation
from userdata.debriefing import Debriefing

from .event import Event


class NavalInterceptEvent(Event):
    STRENGTH_INFLUENCE = 0.3

    targets = None  # type: db.ShipDict

    def _targets_count(self) -> int:
        from gen.conflictgen import IMPORTANCE_LOW, IMPORTANCE_HIGH
        factor = (self.to_cp.importance - IMPORTANCE_LOW) * 10
        return min(int(factor), 1)

    def __str__(self) -> str:
        return "Naval intercept at {}".format(self.to_cp)

    @property
    def threat_description(self):
        s = "{} ship(s)".format(self._targets_count())
        if not self.from_cp.captured:
            s += ", {} aircraft".format(self.from_cp.base.scramble_count())
        return s

    def is_successfull(self, debriefing: Debriefing):
        targets_destroyed = [c for t, c in debriefing.destroyed_units.items() if t in self.targets.values()]
        if self.from_cp.captured:
            return targets_destroyed > 0
        else:
            return targets_destroyed == 0

    def commit(self, debriefing: Debriefing):
        super(NavalInterceptEvent, self).commit(debriefing)

        if self.attacker_name == self.game.player:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
        else:
            # enemy attacking
            if self.is_successfull(debriefing):
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def player_attacking(self, strikegroup: db.PlaneDict, clients: db.PlaneDict):
        self.targets = {
            random.choice(db.find_unittype(CargoTransportation, self.defender_name)): self._targets_count(),
        }

        op = NavalInterceptionOperation(
            self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            attacker_clients=clients,
            defender_clients={},
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        op.setup(strikegroup=strikegroup,
                 interceptors={},
                 targets=self.targets)

        self.operation = op

    def player_defending(self, interceptors: db.PlaneDict, clients: db.PlaneDict):
        self.targets = {
            random.choice(db.find_unittype(CargoTransportation, self.defender_name)): self._targets_count(),
        }

        op = NavalInterceptionOperation(
            self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            attacker_clients=clients,
            defender_clients={},
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        strikegroup = self.from_cp.base.scramble_cas()
        op.setup(strikegroup=strikegroup,
                 interceptors=interceptors,
                 targets=self.targets)

        self.operation = op
