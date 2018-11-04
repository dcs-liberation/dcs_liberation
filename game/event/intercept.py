from game.operation.intercept import InterceptOperation

from .event import *


class InterceptEvent(Event):
    STRENGTH_INFLUENCE = 0.3
    GLOBAL_STRENGTH_INFLUENCE = 0.3
    AIRDEFENSE_COUNT = 3

    transport_unit = None  # type: FlyingType

    def __str__(self):
        return "Air Intercept"

    @property
    def tasks(self):
        return [CAP]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAP:
            if self.is_player_attacking:
                return "Intercept flight"
            else:
                return "Escort flight"

    def _enemy_scramble_multiplier(self) -> float:
        is_global = self.departure_cp.is_global or self.to_cp.is_global
        return self.game.settings.multiplier * is_global and 0.5 or 1

    @property
    def threat_description(self):
        return "{} aircraft".format(self.enemy_cp.base.scramble_count(self._enemy_scramble_multiplier(), CAP))

    def is_successfull(self, debriefing: Debriefing):
        units_destroyed = debriefing.destroyed_units[self.defender_name].get(self.transport_unit, 0)
        if self.departure_cp.captured:
            return units_destroyed > 0
        else:
            return units_destroyed == 0

    def commit(self, debriefing: Debriefing):
        super(InterceptEvent, self).commit(debriefing)

        if self.attacker_name == self.game.player:
            if self.is_successfull(debriefing):
                for _, cp in self.game.theater.conflicts(True):
                    cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.departure_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
        else:
            # enemy attacking
            if self.is_successfull(debriefing):
                self.departure_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)
            else:
                self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def skip(self):
        if self.to_cp.captured:
            self.to_cp.base.affect_strength(-self.STRENGTH_INFLUENCE)

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAP in flights and len(flights) == 1, "Invalid flights"

        escort = self.to_cp.base.scramble_sweep(self._enemy_scramble_multiplier())

        self.transport_unit = random.choice(db.find_unittype(Transport, self.defender_name))
        assert self.transport_unit is not None

        airdefense_unit = db.find_unittype(AirDefence, self.defender_name)[-1]
        op = InterceptOperation(game=self.game,
                                attacker_name=self.attacker_name,
                                defender_name=self.defender_name,
                                from_cp=self.departure_cp,
                                to_cp=self.to_cp)

        op.setup(escort=assigned_units_from(escort),
                 transport={self.transport_unit: 1},
                 airdefense={airdefense_unit: self.AIRDEFENSE_COUNT},
                 interceptors=flights[CAP])

        self.operation = op

    def player_defending(self, flights: db.TaskForceDict):
        assert CAP in flights and len(flights) == 1, "Invalid flights"

        interceptors = self.departure_cp.base.scramble_interceptors(self.game.settings.multiplier)

        self.transport_unit = random.choice(db.find_unittype(Transport, self.defender_name))
        assert self.transport_unit is not None

        op = InterceptOperation(game=self.game,
                                attacker_name=self.attacker_name,
                                defender_name=self.defender_name,
                                from_cp=self.departure_cp,
                                to_cp=self.to_cp)

        op.setup(escort=flights[CAP],
                 transport={self.transport_unit: 1},
                 interceptors=assigned_units_from(interceptors),
                 airdefense={})

        self.operation = op


