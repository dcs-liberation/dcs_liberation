from game.operation.navalintercept import NavalInterceptionOperation

from .event import *


class NavalInterceptEvent(Event):
    STRENGTH_INFLUENCE = 0.3
    SUCCESS_RATE = 0.5

    targets = None  # type: db.ShipDict

    def _targets_count(self) -> int:
        from gen.conflictgen import IMPORTANCE_LOW
        factor = (self.to_cp.importance - IMPORTANCE_LOW) * 10
        return max(int(factor), 1)

    def __str__(self) -> str:
        return "Naval intercept"

    @property
    def tasks(self):
        if self.is_player_attacking:
            return [CAS]
        else:
            return [CAP]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAS:
            return "Naval intercept flight"
        elif for_task == CAP:
            return "CAP flight"

    @property
    def threat_description(self):
        s = "{} ship(s)".format(self._targets_count())
        if not self.from_cp.captured:
            s += ", {} aircraft".format(self.from_cp.base.scramble_count(self.game.settings.multiplier))
        return s

    def is_successfull(self, debriefing: Debriefing):
        total_targets = sum(self.targets.values())
        destroyed_targets = 0
        for unit, count in debriefing.destroyed_units[self.defender_name].items():
            if unit in self.targets:
                destroyed_targets += count

        if self.from_cp.captured:
            return math.ceil(float(destroyed_targets) / total_targets) > self.SUCCESS_RATE
        else:
            return math.ceil(float(destroyed_targets) / total_targets) < self.SUCCESS_RATE

    def commit(self, debriefing: Debriefing):
        super(NavalInterceptEvent, self).commit(debriefing)

        if self.attacker_name == self.game.player:
            if self.is_successfull(debriefing):
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
        else:
            # enemy attacking
            if self.is_successfull(debriefing):
                self.from_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAS in flights and len(flights) == 1, "Invalid flights"

        self.targets = {
            random.choice(db.find_unittype(CargoTransportation, self.defender_name)): self._targets_count(),
        }

        op = NavalInterceptionOperation(
            self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        op.setup(strikegroup=flights[CAS],
                 interceptors={},
                 targets=self.targets)

        self.operation = op

    def player_defending(self, flights: db.TaskForceDict):
        assert CAP in flights and len(flights) == 1, "Invalid flights"

        self.targets = {
            random.choice(db.find_unittype(CargoTransportation, self.defender_name)): self._targets_count(),
        }

        op = NavalInterceptionOperation(
            self.game,
            attacker_name=self.attacker_name,
            defender_name=self.defender_name,
            from_cp=self.from_cp,
            to_cp=self.to_cp
        )

        strikegroup = self.from_cp.base.scramble_cas(self.game.settings.multiplier)
        op.setup(strikegroup=assigned_units_from(strikegroup),
                 interceptors=flights[CAP],
                 targets=self.targets)

        self.operation = op
