from game.operation.strike import StrikeOperation

from .event import *


class StrikeEvent(Event):
    STRENGTH_INFLUENCE = 0.0
    SINGLE_OBJECT_STRENGTH_INFLUENCE = 0.05

    def __str__(self):
        return "Strike / SEAD"

    def is_successfull(self, debriefing: Debriefing):
        return True

    @property
    def threat_description(self):
        return "{} aircraft + AA".format(self.to_cp.base.scramble_count(self.game.settings.multiplier, CAP))

    @property
    def tasks(self):
        if self.is_player_attacking:
            return [CAP, CAS]
        else:
            return [CAP]

    @property
    def ai_banned_tasks(self):
        return [CAS]

    @property
    def global_cp_available(self) -> bool:
        return True

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAP:
            if self.is_player_attacking:
                return "Escort flight"
            else:
                return "CAP flight"
        elif for_task == CAS:
            return "Strike flight"

    def commit(self, debriefing: Debriefing):
        super(StrikeEvent, self).commit(debriefing)

        self.to_cp.base.affect_strength(-self.SINGLE_OBJECT_STRENGTH_INFLUENCE * len(debriefing.destroyed_objects))

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAP in flights and CAS in flights and len(flights) == 2, "Invalid flights"

        op = StrikeOperation(
            self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            from_cp=self.from_cp,
            departure_cp=self.departure_cp,
            to_cp=self.to_cp
        )

        interceptors = self.to_cp.base.scramble_interceptors(self.game.settings.multiplier)
        op.setup(strikegroup=flights[CAS],
                 escort=flights[CAP],
                 interceptors=assigned_units_from(interceptors))

        self.operation = op
