import math
import random

from dcs.task import *

from game import *
from game.event import *
from game.event.groundintercept import GroundInterceptEvent
from game.operation.groundattack import GroundAttackOperation


class GroundAttackEvent(GroundInterceptEvent):
    def __str__(self):
        return "Destroy insurgents at {}".format(self.to_cp)

    @property
    def threat_description(self):
        return ""

    def player_defending(self, strikegroup: db.PlaneDict, clients: db.PlaneDict):
        suitable_unittypes = db.find_unittype(Reconnaissance, self.attacker_name)
        random.shuffle(suitable_unittypes)
        unittypes = suitable_unittypes[:self.TARGET_VARIETY]
        typecount = max(math.floor(self.difficulty * self.TARGET_AMOUNT_FACTOR), 1)
        self.targets = {unittype: typecount for unittype in unittypes}

        op = GroundAttackOperation(game=self.game,
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
