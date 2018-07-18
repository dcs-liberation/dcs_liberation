import math
import random

from dcs.task import *

from game import *
from game.event import *
from game.event.frontlineattack import FrontlineAttackEvent
from game.operation.insurgentattack import InsurgentAttackOperation


class InsurgentAttackEvent(Event):
    SUCCESS_FACTOR = 0.7
    TARGET_VARIETY = 2
    TARGET_AMOUNT_FACTOR = 0.5

    @property
    def threat_description(self):
        return ""

    def __str__(self):
        return "Destroy insurgents at {}".format(self.to_cp)

    def is_successfull(self, debriefing: Debriefing):
        killed_units = sum([v for k, v in debriefing.destroyed_units[self.attacker_name].items() if db.unit_task(k) == PinpointStrike])
        all_units = sum(self.targets.values())
        attackers_success = (float(killed_units) / all_units + 0.01) > self.SUCCESS_FACTOR
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def player_defending(self, strikegroup: db.PlaneDict, clients: db.PlaneDict):
        suitable_unittypes = db.find_unittype(Reconnaissance, self.attacker_name)
        random.shuffle(suitable_unittypes)
        unittypes = suitable_unittypes[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.difficulty * self.TARGET_AMOUNT_FACTOR), 1)
        self.targets = {unittype: typecount for unittype in unittypes}

        op = InsurgentAttackOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      attacker_clients={},
                                      defender_clients=clients,
                                      from_cp=self.from_cp,
                                      to_cp=self.to_cp)
        op.setup(target=self.targets,
                 strikegroup=strikegroup)

        self.operation = op

    def player_attacking(self, interceptors: db.PlaneDict, clients: db.PlaneDict):
        assert False
