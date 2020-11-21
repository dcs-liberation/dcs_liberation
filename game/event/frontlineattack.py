from typing import List, Type

from dcs.task import CAP, CAS, Task
from game.operation.operation import Operation

from ..debriefing import Debriefing
from .event import Event


class FrontlineAttackEvent(Event):

    @property
    def tasks(self) -> List[Type[Task]]:
        if self.is_player_attacking:
            return [CAS, CAP]
        else:
            return [CAP]

    @property
    def global_cp_available(self) -> bool:
        return True

    def __str__(self):
        return "Frontline attack"

    def is_successful(self, debriefing: Debriefing):
        attackers_success = True
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def commit(self, debriefing: Debriefing):
        super(FrontlineAttackEvent, self).commit(debriefing)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-0.1)

    def player_attacking(self):
        assert self.departure_cp is not None
        self.operation = Operation(departure_cp=self.departure_cp,)
