import math
import random

from dcs.task import *

from game import *
from game.event import *
from game.event.frontlineattack import FrontlineAttackEvent
from game.operation.insurgentattack import InsurgentAttackOperation

from .event import *


class InsurgentAttackEvent(Event):
    SUCCESS_FACTOR = 0.7
    TARGET_VARIETY = 2
    TARGET_AMOUNT_FACTOR = 0.5
    STRENGTH_INFLUENCE = 0.1

    @property
    def threat_description(self):
        return ""

    @property
    def tasks(self):
        return [CAS]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAS:
            return "Ground intercept flight"

    def __str__(self):
        return "Destroy insurgents"

    def skip(self):
        self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def is_successfull(self, debriefing: Debriefing):
        killed_units = sum([v for k, v in debriefing.destroyed_units[self.attacker_name].items() if db.unit_task(k) == PinpointStrike])
        all_units = sum(self.targets.values())
        attackers_success = (float(killed_units) / (all_units + 0.01)) > self.SUCCESS_FACTOR
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def player_defending(self, flights: db.TaskForceDict):
        assert CAS in flights and len(flights) == 1, "Invalid flights"

        suitable_unittypes = db.find_unittype(Reconnaissance, self.attacker_name)
        random.shuffle(suitable_unittypes)
        unittypes = suitable_unittypes[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.difficulty * self.TARGET_AMOUNT_FACTOR), 1)
        self.targets = {unittype: typecount for unittype in unittypes}

        op = InsurgentAttackOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      from_cp=self.from_cp,
                                      to_cp=self.to_cp)
        op.setup(target=self.targets,
                 strikegroup=flights[CAS])

        self.operation = op
