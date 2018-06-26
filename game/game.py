import typing
import random
import math

from dcs.task import *
from dcs.vehicles import *

from userdata.debriefing import Debriefing
from theater import *

from . import db
from .settings import Settings
from .event import *

COMMISION_LIMITS_SCALE = 1.5
COMMISION_LIMITS_FACTORS = {
    PinpointStrike: 10,
    CAS: 5,
    CAP: 8,
    AirDefence: 2,
}

COMMISION_AMOUNTS_SCALE = 1.5
COMMISION_UNIT_VARIETY = 4
COMMISION_AMOUNTS_FACTORS = {
    PinpointStrike: 2,
    CAS: 1,
    CAP: 2,
    AirDefence: 0.3,
}

PLAYER_INTERCEPT_GLOBAL_PROBABILITY_BASE = 25
PLAYER_INTERCEPT_GLOBAL_PROBABILITY_LOG = 2
EVENT_PROBABILITIES = {
    CaptureEvent: [100, 4],
    InterceptEvent: [25, 5],
    GroundInterceptEvent: [25, 5],
    GroundAttackEvent: [0, 5],
    NavalInterceptEvent: [25, 5],
    AntiAAStrikeEvent: [25, 5],
    InfantryTransportEvent: [25, 0],
}

PLAYER_BASE_STRENGTH_RECOVERY = 0.2
PLAYER_BUDGET_INITIAL = 120
PLAYER_BUDGET_BASE = 30
PLAYER_BUDGET_IMPORTANCE_LOG = 2

AWACS_BUDGET_COST = 4


class Game:
    settings = None  # type: Settings
    budget = PLAYER_BUDGET_INITIAL
    events = None  # type: typing.List[Event]
    pending_transfers = None  # type: typing.Dict[]
    ignored_cps = None  # type: typing.Collection[ControlPoint]

    def __init__(self, player_name: str, enemy_name: str, theater: ConflictTheater):
        self.settings = Settings()
        self.events = []
        self.theater = theater
        self.player = player_name
        self.enemy = enemy_name

    def _roll(self, prob, mult):
        return random.randint(1, 100) <= prob * mult

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

    def _generate_events(self):
        enemy_cap_generated = False
        enemy_generated_types = []

        for player_cp, enemy_cp in self.theater.conflicts(True):
            if player_cp.is_global or enemy_cp.is_global:
                continue

            for event_class, (player_probability, enemy_probability) in EVENT_PROBABILITIES.items():
                if self._roll(player_probability, player_cp.base.strength):
                    if event_class == NavalInterceptEvent:
                        if enemy_cp.radials == LAND:
                            continue

                    self.events.append(event_class(self.player, self.enemy, player_cp, enemy_cp, self))
                elif self._roll(enemy_probability, enemy_cp.base.strength):
                    if event_class in enemy_generated_types:
                        continue

                    if player_cp in self.ignored_cps:
                        continue

                    if enemy_cp.base.total_planes == 0:
                        continue

                    if event_class == NavalInterceptEvent:
                        if player_cp.radials == LAND:
                            continue
                    elif event_class == CaptureEvent:
                        if enemy_cap_generated:
                            continue
                        if enemy_cp.base.total_armor == 0:
                            continue
                        enemy_cap_generated = True
                    elif event_class == AntiAAStrikeEvent:
                        if player_cp.base.total_aa == 0:
                            continue

                    enemy_generated_types.append(event_class)
                    self.events.append(event_class(self.enemy, self.player, enemy_cp, player_cp, self))

    def _commision_units(self, cp: ControlPoint):
        for for_task in [PinpointStrike, CAS, CAP, AirDefence]:
            limit = COMMISION_LIMITS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_LIMITS_SCALE) * self.settings.multiplier
            missing_units = limit - cp.base.total_units(for_task)
            if missing_units > 0:
                awarded_points = COMMISION_AMOUNTS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_AMOUNTS_SCALE) * self.settings.multiplier
                points_to_spend = cp.base.append_commision_points(for_task, awarded_points)
                if points_to_spend > 0:
                    importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)

                    if for_task == AirDefence and not self.settings.sams:
                        unittypes = [x for x in db.find_unittype(AirDefence, self.enemy) if x not in db.SAM_BAN]
                    else:
                        unittypes = db.choose_units(for_task, importance_factor, COMMISION_UNIT_VARIETY, self.enemy)

                    d = {random.choice(unittypes): points_to_spend}
                    print("Commision {}: {}".format(cp, d))
                    cp.base.commision_units(d)

    @property
    def budget_reward_amount(self):
        if len(self.theater.player_points()) > 0:
            total_importance = sum([x.importance for x in self.theater.player_points()])
            total_strength = sum([x.base.strength for x in self.theater.player_points()]) / len(self.theater.player_points())
            return math.ceil(math.log(total_importance * total_strength + 1, PLAYER_BUDGET_IMPORTANCE_LOG) * PLAYER_BUDGET_BASE * self.settings.multiplier)
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

        if event in self.events:
            self.events.remove(event)
        else:
            print("finish_event: event not in the events!")

    def is_player_attack(self, event: Event):
        return event.attacker_name == self.player

    def pass_turn(self, no_action=False, ignored_cps: typing.Collection[ControlPoint]=None):
        for event in self.events:
            event.skip()

        if not no_action:
            self._budget_player()
            for cp in self.theater.enemy_points():
                self._commision_units(cp)
            for cp in self.theater.player_points():
                cp.base.affect_strength(+PLAYER_BASE_STRENGTH_RECOVERY)

        self.ignored_cps = []
        if ignored_cps:
            self.ignored_cps = ignored_cps

        self.events = []  # type: typing.List[Event]
        self._generate_events()
        self._generate_globalinterceptions()

