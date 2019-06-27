from game.operation.baseattack import BaseAttackOperation

from .event import *
from game.db import assigned_units_from


class BaseAttackEvent(Event):
    silent = True
    BONUS_BASE = 15
    STRENGTH_RECOVERY = 0.55

    def __str__(self):
        return "Base attack"

    @property
    def tasks(self):
        return [CAP, CAS, PinpointStrike]

    def flight_name(self, for_task: typing.Type[Task]) -> str:
        if for_task == CAP:
            return "Escort flight"
        elif for_task == CAS:
            return "CAS flight"
        elif for_task == PinpointStrike:
            return "Ground attack"

    def is_successfull(self, debriefing: Debriefing):
        alive_attackers = sum([v for k, v in debriefing.alive_units.get(self.attacker_name, {}).items() if db.unit_task(k) == PinpointStrike])
        alive_defenders = sum([v for k, v in debriefing.alive_units.get(self.defender_name, {}).items() if db.unit_task(k) == PinpointStrike])
        attackers_success = alive_attackers >= alive_defenders
        if self.departure_cp.captured:
            return attackers_success
        else:
            return not attackers_success

    def commit(self, debriefing: Debriefing):
        super(BaseAttackEvent, self).commit(debriefing)
        if self.is_successfull(debriefing):
            if self.departure_cp.captured:
                self.to_cp.captured = True
                self.to_cp.ground_objects = []
                self.to_cp.base.filter_units(db.UNIT_BY_COUNTRY[self.attacker_name])

            self.to_cp.base.affect_strength(+self.STRENGTH_RECOVERY)
        else:
            if not self.departure_cp.captured:
                self.to_cp.captured = False
            self.to_cp.base.affect_strength(+self.STRENGTH_RECOVERY)

    def skip(self):
        if not self.is_player_attacking and self.to_cp.captured:
            self.to_cp.captured = False

    def player_defending(self, flights: db.TaskForceDict):
        assert CAP in flights and len(flights) == 1,  "Invalid scrambled flights"

        cas = self.departure_cp.base.scramble_cas(self.game.settings.multiplier)
        escort = self.departure_cp.base.scramble_sweep(self.game.settings.multiplier)
        attackers = self.departure_cp.base.armor

        op = BaseAttackOperation(game=self.game,
                                 attacker_name=self.attacker_name,
                                 defender_name=self.defender_name,
                                 from_cp=self.from_cp,
                                 departure_cp=self.departure_cp,
                                 to_cp=self.to_cp)

        op.setup(cas=assigned_units_from(cas),
                 escort=assigned_units_from(escort),
                 intercept=flights[CAP],
                 attack=attackers,
                 defense=self.to_cp.base.armor,
                 aa=self.to_cp.base.aa)

        self.operation = op

    def player_attacking(self, flights: db.TaskForceDict):
        assert CAP in flights and CAS in flights and PinpointStrike in flights and len(flights) == 3, "Invalid flights"

        op = BaseAttackOperation(game=self.game,
                                 attacker_name=self.attacker_name,
                                 defender_name=self.defender_name,
                                 from_cp=self.from_cp,
                                 departure_cp=self.departure_cp,
                                 to_cp=self.to_cp)

        defenders = self.to_cp.base.scramble_last_defense()
        #defenders.update(self.to_cp.base.scramble_cas(self.game.settings.multiplier))

        op.setup(cas=flights[CAS],
                 escort=flights[CAP],
                 attack=unitdict_from(flights[PinpointStrike]),
                 intercept=assigned_units_from(defenders),
                 defense=self.to_cp.base.armor,
                 aa=self.to_cp.base.assemble_aa())

        self.operation = op

