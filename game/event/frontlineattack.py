from game.event import *
from game.operation.frontlineattack import FrontlineAttackOperation
from userdata.debriefing import Debriefing


class FrontlineAttackEvent(Event):

    @property
    def tasks(self) -> typing.Collection[typing.Type[Task]]:
        if self.is_player_attacking:
            return [CAS, CAP]
        else:
            return [CAP]

    @property
    def global_cp_available(self) -> bool:
        return True

    def __str__(self):
        return "Frontline attack"

    def is_successfull(self, debriefing: Debriefing):
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

    def player_attacking(self, flights: db.TaskForceDict):
        op = FrontlineAttackOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      from_cp=self.from_cp,
                                      departure_cp=self.departure_cp,
                                      to_cp=self.to_cp)
        self.operation = op

    def player_defending(self, flights: db.TaskForceDict):
        op = FrontlineAttackOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      from_cp=self.from_cp,
                                      departure_cp=self.departure_cp,
                                      to_cp=self.to_cp)
        self.operation = op

