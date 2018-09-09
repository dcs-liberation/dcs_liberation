import math
import random

from dcs.task import *
from dcs.vehicles import *

from game import db
from game.operation.infantrytransport import InfantryTransportOperation
from theater.conflicttheater import *
from userdata.debriefing import Debriefing

from .event import *


class InfantryTransportEvent(Event):
    STRENGTH_INFLUENCE = 0.3

    def __str__(self):
        return "Frontline transport troops"

    @property
    def tasks(self):
        return [Embarking]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == Embarking:
            return "Transport flight"

    def is_successfull(self, debriefing: Debriefing):
        return True

    def commit(self, debriefing: Debriefing):
        super(InfantryTransportEvent, self).commit(debriefing)

        if self.is_successfull(debriefing):
            self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
        else:
            self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def player_attacking(self, flights: ScrambledFlightsDict):
        assert flights[Embarking] and len(flights) == 1, "Invalid flights"

        op = InfantryTransportOperation(
            game=self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        air_defense = db.find_unittype(AirDefence, self.defender_name)[0]
        op.setup(transport=flights[Embarking],
                 aa={air_defense: 2})

        self.operation = op
