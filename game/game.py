import typing
import random
import math

from dcs.task import *
from dcs.vehicles import *

from userdata.debriefing import Debriefing
from theater import *

from . import db
from .event import *

COMMISION_LIMITS_SCALE = 2
COMMISION_LIMITS_FACTORS = {
    PinpointStrike: 2,
    CAS: 1,
    CAP: 3,
    AirDefence: 1,
}

COMMISION_AMOUNTS_SCALE = 2
COMMISION_UNIT_VARIETY = 4
COMMISION_AMOUNTS_FACTORS = {
    PinpointStrike: 0.6,
    CAS: 0.3,
    CAP: 0.5,
    AirDefence: 0.3,
}


ENEMY_INTERCEPT_PROBABILITY_BASE = 8
ENEMY_INTERCEPT_GLOBAL_PROBABILITY_BASE = 5
ENEMY_CAPTURE_PROBABILITY_BASE = 4
ENEMY_GROUNDINTERCEPT_PROBABILITY_BASE = 8
ENEMY_NAVALINTERCEPT_PROBABILITY_BASE = 8

PLAYER_INTERCEPT_PROBABILITY_BASE = 35
PLAYER_GROUNDINTERCEPT_PROBABILITY_BASE = 35
PLAYER_NAVALINTERCEPT_PROBABILITY_BASE = 35
PLAYER_INTERCEPT_GLOBAL_PROBABILITY_BASE = 25
PLAYER_INTERCEPT_GLOBAL_PROBABILITY_LOG = 2

PLAYER_BUDGET_INITIAL = 90
PLAYER_BUDGET_BASE = 20
PLAYER_BUDGET_IMPORTANCE_LOG = 2

AWACS_BUDGET_COST = 4


class Game:
    budget = PLAYER_BUDGET_INITIAL
    events = None  # type: typing.List[Event]
    pending_transfers = None  # type: typing.Dict[]
    player_skill = "Good"
    enemy_skill = "Average"

    def __init__(self, player_name: str, enemy_name: str, theater: ConflictTheater):
        self.events = []
        self.theater = theater
        self.player = player_name
        self.enemy = enemy_name

    def _roll(self, prob, mult):
        return random.randint(0, 100) <= prob * mult

    def _fill_cap_events(self):
        for from_cp, to_cp in self.theater.conflicts(True):
            if to_cp not in [x.to_cp for x in self.events]:
                self.events.append(CaptureEvent(attacker_name=self.player,
                                                defender_name=self.enemy,
                                                from_cp=from_cp,
                                                to_cp=to_cp,
                                                game=self))

    def _generate_enemy_caps(self, ignored_cps: typing.Collection[ControlPoint] = None):
        for from_cp, to_cp in self.theater.conflicts(False):
            if from_cp.base.total_planes == 0 or from_cp.base.total_armor == 0:
                continue

            if ignored_cps and to_cp in ignored_cps:
                continue

            if self._roll(ENEMY_CAPTURE_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(CaptureEvent(attacker_name=self.enemy,
                                                defender_name=self.player,
                                                from_cp=from_cp,
                                                to_cp=to_cp,
                                                game=self))
                break

    def _generate_interceptions(self):
        enemy_interception = False
        for from_cp, to_cp in self.theater.conflicts(False):
            if from_cp.base.total_units(CAP) == 0:
                continue

            if self._roll(ENEMY_INTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(InterceptEvent(attacker_name=self.enemy,
                                                  defender_name=self.player,
                                                  from_cp=from_cp,
                                                  to_cp=to_cp,
                                                  game=self))
                enemy_interception = True
                break

            if to_cp in self.theater.conflicts(False):
                continue

            if self._roll(ENEMY_INTERCEPT_GLOBAL_PROBABILITY_BASE, 1):
                for from_cp, _ in self.theater.conflicts(False):
                    if from_cp.base.total_units(CAP) > 0:
                        self.events.append(InterceptEvent(attacker_name=self.enemy,
                                                          defender_name=self.player,
                                                          from_cp=from_cp,
                                                          to_cp=to_cp,
                                                          game=self))
                        enemy_interception = True
                        break

        for from_cp, to_cp in self.theater.conflicts(True):
            if self._roll(PLAYER_INTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(InterceptEvent(attacker_name=self.player,
                                                  defender_name=self.enemy,
                                                  from_cp=from_cp,
                                                  to_cp=to_cp,
                                                  game=self))
                break

    def _generate_groundinterceptions(self):
        for from_cp, to_cp in self.theater.conflicts(True):
            if self._roll(PLAYER_GROUNDINTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(GroundInterceptEvent(attacker_name=self.player,
                                                        defender_name=self.enemy,
                                                        from_cp=from_cp,
                                                        to_cp=to_cp,
                                                        game=self))
                break

        for from_cp, to_cp in self.theater.conflicts(False):
            if self._roll(ENEMY_GROUNDINTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(GroundInterceptEvent(attacker_name=self.enemy,
                                                        defender_name=self.player,
                                                        from_cp=from_cp,
                                                        to_cp=to_cp,
                                                        game=self))
                break

    def _generate_navalinterceptions(self):
        for from_cp, to_cp in self.theater.conflicts(True):
            if to_cp.radials == LAND:
                continue

            if self._roll(PLAYER_NAVALINTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(NavalInterceptEvent(attacker_name=self.player,
                                                       defender_name=self.enemy,
                                                       from_cp=from_cp,
                                                       to_cp=to_cp,
                                                       game=self))
                break

        for from_cp, to_cp in self.theater.conflicts(False):
            if to_cp.radials == LAND:
                continue

            if self._roll(ENEMY_NAVALINTERCEPT_PROBABILITY_BASE, from_cp.base.strength):
                self.events.append(NavalInterceptEvent(attacker_name=self.enemy,
                                                       defender_name=self.player,
                                                       from_cp=from_cp,
                                                       to_cp=to_cp,
                                                       game=self))
                break

    def _generate_globalinterceptions(self):
        global_count = len([x for x in self.theater.player_points() if x.is_global])
        for from_cp in [x for x in self.theater.player_points() if x.is_global]:
            probability_base = max(PLAYER_INTERCEPT_GLOBAL_PROBABILITY_BASE / global_count, 1)
            probability = probability_base * math.log(len(self.theater.player_points()) + 1, PLAYER_INTERCEPT_GLOBAL_PROBABILITY_LOG)
            if self._roll(probability, from_cp.base.strength):
                to_cp = random.choice([x for x in self.theater.enemy_points() if x not in self.theater.conflicts()])
                self.events.append(InterceptEvent(attacker_name=self.player,
                                                  defender_name=self.enemy,
                                                  from_cp=from_cp,
                                                  to_cp=to_cp,
                                                  game=self))
                break

    def _commision_units(self, cp: ControlPoint):
        for for_task in [PinpointStrike, CAS, CAP, AirDefence]:
            limit = COMMISION_LIMITS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_LIMITS_SCALE)
            missing_units = limit - cp.base.total_units(for_task)
            if missing_units > 0:
                awarded_points = COMMISION_AMOUNTS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_AMOUNTS_SCALE)
                points_to_spend = cp.base.append_commision_points(for_task, awarded_points)
                if points_to_spend > 0:
                    importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)
                    unittypes = db.choose_units(for_task, importance_factor, COMMISION_UNIT_VARIETY, self.enemy)
                    cp.base.commision_units({random.choice(unittypes): points_to_spend})

    @property
    def budget_reward_amount(self):
        if len(self.theater.player_points()) > 0:
            total_importance = sum([x.importance for x in self.theater.player_points()])
            total_strength = sum([x.base.strength for x in self.theater.player_points()]) / len(self.theater.player_points())
            return math.ceil(math.log(total_importance * total_strength + 1, PLAYER_BUDGET_IMPORTANCE_LOG) * PLAYER_BUDGET_BASE)
        else:
            return 0

    def _budget_player(self):
        self.budget += self.budget_reward_amount

    def awacs_expense_commit(self):
        self.budget -= AWACS_BUDGET_COST

    def units_delivery_event(self, to_cp: ControlPoint) -> UnitsDeliveryEvent:
        event = UnitsDeliveryEvent(attacker_name=self.player,
                                   defender_name=self.player,
                                   from_cp=to_cp,
                                   to_cp=to_cp,
                                   game=self)
        self.events.append(event)
        return event

    def units_delivery_remove(self, event: Event):
        if event in self.events:
            self.events.remove(event)

    def initiate_event(self, event: Event):
        assert event in self.events

        event.generate()
        event.generate_quick()

    def finish_event(self, event: Event, debriefing: Debriefing):
        event.commit(debriefing)
        if event.is_successfull(debriefing):
            self.budget += event.bonus()

        self.events.remove(event)

    def is_player_attack(self, event: Event):
        return event.attacker_name == self.player

    def pass_turn(self, no_action=False, ignored_cps: typing.Collection[ControlPoint]=None):
        for event in self.events:
            event.skip()

        if not no_action:
            self._budget_player()
            for cp in self.theater.enemy_points():
                self._commision_units(cp)

        self.events = []  # type: typing.List[Event]
        self._fill_cap_events()
        #self._generate_enemy_caps(ignored_cps=ignored_cps)
        self._generate_interceptions()
        self._generate_globalinterceptions()
        self._generate_groundinterceptions()
        self._generate_navalinterceptions()

