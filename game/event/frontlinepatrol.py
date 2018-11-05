from game.event import *
from game.operation.frontlinepatrol import FrontlinePatrolOperation
from userdata.debriefing import Debriefing


class FrontlinePatrolEvent(Event):
    ESCORT_FACTOR = 0.5
    STRENGTH_INFLUENCE = 0.3
    SUCCESS_FACTOR = 0.8

    cas = None  # type: db.PlaneDict
    escort = None  # type: db.PlaneDict

    @property
    def threat_description(self):
        return "{} aircraft + ? CAS".format(self.to_cp.base.scramble_count(self.game.settings.multiplier * self.ESCORT_FACTOR, CAP))

    @property
    def tasks(self):
        return [CAP]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAP:
            return "CAP flight"
        elif for_task == PinpointStrike:
            return "Ground attack"

    def __str__(self):
        return "Frontline CAP"

    def is_successfull(self, debriefing: Debriefing):
        alive_attackers = sum([v for k, v in debriefing.alive_units[self.attacker_name].items() if db.unit_task(k) == PinpointStrike])
        alive_defenders = sum([v for k, v in debriefing.alive_units[self.defender_name].items() if db.unit_task(k) == PinpointStrike])
        attackers_success = (float(alive_attackers) / (alive_defenders + 0.01)) >= self.SUCCESS_FACTOR
        if self.from_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def commit(self, debriefing: Debriefing):
        super(FrontlinePatrolEvent, self).commit(debriefing)

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
        pass

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAP in flights and len(flights) == 1, "Invalid flights"

        self.cas = self.to_cp.base.scramble_cas(self.game.settings.multiplier)
        self.escort = self.to_cp.base.scramble_sweep(self.game.settings.multiplier * self.ESCORT_FACTOR)

        op = FrontlinePatrolOperation(game=self.game,
                                      attacker_name=self.attacker_name,
                                      defender_name=self.defender_name,
                                      from_cp=self.from_cp,
                                      departure_cp=self.departure_cp,
                                      to_cp=self.to_cp)

        defenders = self.to_cp.base.assemble_attack()
        attackers = db.unitdict_restrict_count(self.from_cp.base.assemble_attack(), sum(defenders.values()))
        op.setup(cas=assigned_units_from(self.cas),
                 escort=assigned_units_from(self.escort),
                 interceptors=flights[CAP],
                 armor_attackers=attackers,
                 armor_defenders=defenders)

        self.operation = op
