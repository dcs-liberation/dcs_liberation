import math
import random

from dcs.task import *
from dcs.vehicles import *

from game import db
from game.operation.infantrytransport import InfantryTransportOperation
from theater.conflicttheater import *
from userdata.debriefing import Debriefing

from .event import Event


class InfantryTransportEvent(Event):
    STRENGTH_INFLUENCE = 0.3

    def __str__(self):
        return "Frontline transport troops to {}".format(self.to_cp)

    def is_successfull(self, debriefing: Debriefing):
        return True

    def commit(self, debriefing: Debriefing):
        super(InfantryTransportEvent, self).commit(debriefing)

        if self.is_successfull(debriefing):
            self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
        else:
            self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def player_attacking(self, transport: db.HeliDict, clients: db.HeliDict):
        op = InfantryTransportOperation(
            game=self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            attacker_clients=clients,
            defender_clients={},
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        op.setup(transport=transport)

        self.operation = op
