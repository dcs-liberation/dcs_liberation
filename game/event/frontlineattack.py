from game.event import *
from game.operation.frontlineattack import FrontlineAttackOperation
from userdata.debriefing import Debriefing


class FrontlineAttackEvent(Event):
    TARGET_VARIETY = 2
    TARGET_AMOUNT_FACTOR = 0.5
    ATTACKER_AMOUNT_FACTOR = 0.4
    ATTACKER_DEFENDER_FACTOR = 0.7
    STRENGTH_INFLUENCE = 0.3
    SUCCESS_FACTOR = 1.5

    @property
    def threat_description(self):
        return "{} vehicles".format(self.to_cp.base.assemble_count())

    @property
    def tasks(self) -> typing.Collection[typing.Type[Task]]:
        if self.is_player_attacking:
            return [CAS]
        else:
            return [CAP]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAS:
            return "CAS flight"
        elif for_task == CAP:
            return "CAP flight"
        elif for_task == PinpointStrike:
            return "Ground attack"

    def __str__(self):
        return "Frontline attack"

    def is_successfull(self, debriefing: Debriefing):
        alive_attackers = sum([v for k, v in debriefing.alive_units[self.attacker_name].items() if db.unit_task(k) == PinpointStrike])
        alive_defenders = sum([v for k, v in debriefing.alive_units[self.defender_name].items() if db.unit_task(k) == PinpointStrike])
        attackers_success = (float(alive_attackers) / (alive_defenders + 0.01)) > self.SUCCESS_FACTOR
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def commit(self, debriefing: Debriefing):
        super(FrontlineAttackEvent, self).commit(debriefing)

        if self.from_cp.captured:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(+self.STRENGTH_INFLUENCE)
        else:
            if self.is_successfull(debriefing):
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-0.1)

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAS in flights and len(flights) == 1, "Invalid flights"


        op = FrontlineAttackOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      from_cp=self.from_cp,
                                      departure_cp=self.departure_cp,
                                      to_cp=self.to_cp)

        defenders = self.to_cp.base.assemble_attack()
        attackers = db.unitdict_restrict_count(self.from_cp.base.assemble_attack(), sum(defenders.values()))
        op.setup(target=defenders,
                 attackers=attackers,
                 strikegroup=flights[CAS])

        self.operation = op

