import math
import random

from dcs.task import *
from dcs.vehicles import *

from game import db
from game.operation.strike import StrikeOperation
from theater.conflicttheater import *
from userdata.debriefing import Debriefing

from .event import Event


class StrikeEvent(Event):
    STRENGTH_INFLUENCE = 0.0
    SINGLE_OBJECT_STRENGTH_INFLUENCE = 0.03

    def __str__(self):
        return "Strike"

    def is_successfull(self, debriefing: Debriefing):
        return True

    def commit(self, debriefing: Debriefing):
        super(StrikeEvent, self).commit(debriefing)
        self.to_cp.base.affect_strength(-self.SINGLE_OBJECT_STRENGTH_INFLUENCE * len(debriefing.destroyed_objects))

    def player_attacking(self, strikegroup: db.PlaneDict, escort: db.PlaneDict, clients: db.PlaneDict):
        op = StrikeOperation(
            self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            attacker_clients=clients,
            defender_clients={},
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        interceptors = self.to_cp.base.scramble_interceptors(self.game.settings.multiplier)

        op.setup(strikegroup=strikegroup,
                 escort=escort,
                 interceptors=interceptors)

        self.operation = op
