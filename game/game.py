import typing
import random

from theater.conflicttheater import *
from theater.controlpoint import *
from userdata.debriefing_parser import *
from game.event import *

COMMISION_LIMITS_SCALE = 2
COMMISION_LIMITS_FACTORS = {
    CAP: 2,
    CAS: 1,
    FighterSweep: 3,
    AirDefence: 2,
}

COMMISION_AMOUNTS_SCALE = 2
COMMISION_AMOUNTS_FACTORS = {
    CAP: 0.6,
    CAS: 0.3,
    FighterSweep: 0.5,
    AirDefence: 0.3,
}


ENEMY_INTERCEPT_PROBABILITY_BASE = 25
ENEMY_CAPTURE_PROBABILITY_BASE = 15

PLAYER_INTERCEPT_PROBABILITY_BASE = 30
PLAYER_GROUNDINTERCEPT_PROBABILITY_BASE = 30

PLAYER_BUDGET_BASE = 25
PLAYER_BUDGET_IMPORTANCE_LOG = 2


class Game:
    budget = 45
    events = None  # type: typing.List[Event]

    def __init__(self, theater: ConflictTheater):
        self.events = []
        self.theater = theater
        self.player = "USA"
        self.enemy = "Russia"

    def _roll(self, prob, mult):
        return random.randint(0, 100) <= prob * mult

    def _fill_cap_events(self):
        for from_cp, to_cp in self.theater.conflicts(True):
            self.events.append(CaptureEvent(attacker_name=self.player,
                                            defender_name=self.enemy,
                                            from_cp=from_cp,
                                            to_cp=to_cp))

    def _generate_enemy_caps(self):
        for from_cp, to_cp in self.theater.conflicts(False):
            if self._roll(ENEMY_CAPTURE_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(CaptureEvent(attacker_name=self.enemy,
                                                defender_name=self.player,
                                                from_cp=from_cp,
                                                to_cp=to_cp))
                break

    def _generate_interceptions(self):
        for from_cp, to_cp in self.theater.conflicts(False):
            if self._roll(ENEMY_INTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(InterceptEvent(attacker_name=self.enemy,
                                                  defender_name=self.player,
                                                  from_cp=from_cp,
                                                  to_cp=to_cp))
                break

        for from_cp, to_cp in self.theater.conflicts(True):
            if self._roll(PLAYER_INTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(InterceptEvent(attacker_name=self.player,
                                                  defender_name=self.enemy,
                                                  from_cp=from_cp,
                                                  to_cp=to_cp))
                break

    def _generate_groundinterceptions(self):
        for from_cp, to_cp in self.theater.conflicts(True):
            if self._roll(PLAYER_GROUNDINTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(GroundInterceptEvent(attacker_name=self.player,
                                                        defender_name=self.enemy,
                                                        from_cp=from_cp,
                                                        to_cp=to_cp))
                break

    def _commision_units(self, cp: ControlPoint):
        for for_task in [CAP, CAS, FighterSweep, AirDefence]:
            limit = COMMISION_LIMITS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_LIMITS_SCALE)
            missing_units = limit - cp.base.total_units(for_task)
            if missing_units > 0:
                awarded_points = COMMISION_AMOUNTS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_AMOUNTS_SCALE)
                points_to_spend = cp.base.append_commision_points(for_task, awarded_points)
                if points_to_spend > 0:
                    unit_type = random.choice(db.find_unittype(for_task, self.enemy))
                    cp.base.commision_units({unit_type: points_to_spend})

    def _budget_player(self):
        total_importance = sum([x.importance for x in self.theater.player_points()])
        total_strength = sum([x.base.strength for x in self.theater.player_points()]) / len(self.theater.player_points())

        self.budget += math.ceil(math.log(total_importance * total_strength + 1, PLAYER_BUDGET_IMPORTANCE_LOG) * PLAYER_BUDGET_BASE)

    def initiate_event(self, event: Event):
        event.operation.generate()
        event.mission.save("build/next_mission.miz")

    def finish_event(self, event: Event, debriefing: Debriefing):
        event.commit(debriefing)
        if event.is_successfull(debriefing):
            self.budget += event.bonus()

        self.events.remove(event)

    def is_player_attack(self, event: Event):
        return event.attacker.name == self.player

    def pass_turn(self):
        for event in self.events:
            event.skip()

        self._budget_player()
        for cp in self.theater.enemy_bases():
            self._commision_units(cp)

        self.events = []  # type: typing.List[Event]
        self._fill_cap_events()
        self._generate_enemy_caps()
        self._generate_interceptions()
        self._generate_groundinterceptions()

