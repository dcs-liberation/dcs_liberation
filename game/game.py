import logging
import typing
import random
import math

from dcs.task import *
from dcs.vehicles import *

from gen.conflictgen import Conflict
from userdata.debriefing import Debriefing
from theater import *

from . import db
from .settings import Settings
from .event import *

COMMISION_UNIT_VARIETY = 4
COMMISION_LIMITS_SCALE = 1.5
COMMISION_LIMITS_FACTORS = {
    PinpointStrike: 10,
    CAS: 5,
    CAP: 8,
    AirDefence: 8,
}

COMMISION_AMOUNTS_SCALE = 1.5
COMMISION_AMOUNTS_FACTORS = {
    PinpointStrike: 3,
    CAS: 1,
    CAP: 2,
    AirDefence: 0.8,
}

PLAYER_INTERCEPT_GLOBAL_PROBABILITY_BASE = 30
PLAYER_INTERCEPT_GLOBAL_PROBABILITY_LOG = 2
PLAYER_BASEATTACK_THRESHOLD = 0.4

"""
Various events probabilities. First key is player probabilty, second is enemy probability.
For the enemy events, only 1 event of each type could be generated for a turn.

Events:
* BaseAttackEvent - capture base
* InterceptEvent - air intercept
* FrontlineAttackEvent - frontline attack
* NavalInterceptEvent - naval intercept
* StrikeEvent - strike event
* InfantryTransportEvent - helicopter infantry transport
"""
EVENT_PROBABILITIES = {
    # events always present; only for the player
    FrontlineAttackEvent: [100, 9],
    #FrontlinePatrolEvent: [100, 0],
    StrikeEvent: [100, 0],

    # events randomly present; only for the player
    #InfantryTransportEvent: [25, 0],
    ConvoyStrikeEvent: [25, 0],

    # events conditionally present; for both enemy and player
    BaseAttackEvent: [100, 9],

    # events randomly present; for both enemy and player
    InterceptEvent: [25, 9],
    NavalInterceptEvent: [25, 9],

    # events randomly present; only for the enemy
    InsurgentAttackEvent: [0, 6],
}

# amount of strength player bases recover for the turn
PLAYER_BASE_STRENGTH_RECOVERY = 0.2

# amount of strength enemy bases recover for the turn
ENEMY_BASE_STRENGTH_RECOVERY = 0.05

# cost of AWACS for single operation
AWACS_BUDGET_COST = 4

# Initial budget value
PLAYER_BUDGET_INITIAL = 170
# Base post-turn bonus value
PLAYER_BUDGET_BASE = 14
# Bonus multiplier logarithm base
PLAYER_BUDGET_IMPORTANCE_LOG = 2


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
        if self.settings.version == "dev":
            # always generate all events for dev
            return 100
        else:
            return random.randint(1, 100) <= prob * mult

    def _generate_player_event(self, event_class, player_cp, enemy_cp):
        if event_class == NavalInterceptEvent and enemy_cp.radials == LAND:
            # skip naval events for non-coastal CPs
            return

        if event_class == BaseAttackEvent and enemy_cp.base.strength > PLAYER_BASEATTACK_THRESHOLD and self.settings.version != "dev":
            # skip base attack events for CPs yet too strong
            return

        if event_class == StrikeEvent and not enemy_cp.ground_objects:
            # skip strikes in case of no targets
            return

        self.events.append(event_class(self, player_cp, enemy_cp, enemy_cp.position, self.player, self.enemy))

    def _generate_enemy_event(self, event_class, player_cp, enemy_cp):
        if event_class in [type(x) for x in self.events if not self.is_player_attack(x)]:
            # skip already generated enemy event types
            return

        if player_cp in self.ignored_cps:
            # skip attacks against ignored CPs (for example just captured ones)
            return

        if enemy_cp.base.total_planes == 0:
            # skip event if there's no planes on the base
            return

        if player_cp.is_global:
            # skip carriers
            return

        if event_class == NavalInterceptEvent:
            if player_cp.radials == LAND:
                # skip naval events for non-coastal CPs
                return
        elif event_class == StrikeEvent:
            if not player_cp.ground_objects:
                # skip strikes if there's no ground objects
                return
        elif event_class == BaseAttackEvent:
            if BaseAttackEvent in [type(x) for x in self.events]:
                # skip base attack event if there's another one going on
                return

            if enemy_cp.base.total_armor == 0:
                # skip base attack if there's no armor
                return

            if player_cp.base.strength > PLAYER_BASEATTACK_THRESHOLD:
                # skip base attack if strength is too high
                return

        self.events.append(event_class(self, enemy_cp, player_cp, player_cp.position, self.enemy, self.player))

    def _generate_events(self):
        strikes_generated_for = set()
        base_attack_generated_for = set()

        for player_cp, enemy_cp in self.theater.conflicts(True):
            for event_class, (player_probability, enemy_probability) in EVENT_PROBABILITIES.items():
                if event_class in [FrontlineAttackEvent, FrontlinePatrolEvent, InfantryTransportEvent, ConvoyStrikeEvent]:
                    # skip events requiring frontline
                    if not Conflict.has_frontline_between(player_cp, enemy_cp):
                        continue

                # don't generate multiple 100% events from each attack direction
                if event_class is StrikeEvent:
                    if enemy_cp in strikes_generated_for:
                        continue
                if event_class is BaseAttackEvent:
                    if enemy_cp in base_attack_generated_for:
                        continue

                if player_probability == 100 or player_probability > 0 and self._roll(player_probability, player_cp.base.strength):
                    self._generate_player_event(event_class, player_cp, enemy_cp)
                    if event_class is StrikeEvent:
                        strikes_generated_for.add(enemy_cp)
                    if event_class is BaseAttackEvent:
                        base_attack_generated_for.add(enemy_cp)

                if enemy_probability == 100 or enemy_probability > 0 and self._roll(enemy_probability, enemy_cp.base.strength):
                    self._generate_enemy_event(event_class, player_cp, enemy_cp)

    def commision_unit_types(self, cp: ControlPoint, for_task: Task) -> typing.Collection[UnitType]:
        importance_factor = (cp.importance - IMPORTANCE_LOW) / (IMPORTANCE_HIGH - IMPORTANCE_LOW)

        if for_task == AirDefence and not self.settings.sams:
            return [x for x in db.find_unittype(AirDefence, self.enemy) if x not in db.SAM_BAN]
        else:
            return db.choose_units(for_task, importance_factor, COMMISION_UNIT_VARIETY, self.enemy)

    def _commision_units(self, cp: ControlPoint):
        for for_task in [PinpointStrike, CAS, CAP, AirDefence]:
            limit = COMMISION_LIMITS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_LIMITS_SCALE) * self.settings.multiplier
            missing_units = limit - cp.base.total_units(for_task)
            if missing_units > 0:
                awarded_points = COMMISION_AMOUNTS_FACTORS[for_task] * math.pow(cp.importance, COMMISION_AMOUNTS_SCALE) * self.settings.multiplier
                points_to_spend = cp.base.append_commision_points(for_task, awarded_points)
                if points_to_spend > 0:
                    unittypes = self.commision_unit_types(cp, for_task)
                    d = {random.choice(unittypes): points_to_spend}
                    logging.info("Commision {}: {}".format(cp, d))
                    cp.base.commision_units(d)

    @property
    def budget_reward_amount(self):
        if len(self.theater.player_points()) > 0:
            total_importance = sum([x.importance * x.base.strength for x in self.theater.player_points()])
            return math.ceil(math.log(total_importance + 1, PLAYER_BUDGET_IMPORTANCE_LOG) * PLAYER_BUDGET_BASE * self.settings.multiplier)
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

        logging.info("Generating {} (regular)".format(event))
        event.generate()
        logging.info("Generating {} (quick)".format(event))
        event.generate_quick()

    def finish_event(self, event: Event, debriefing: Debriefing):
        logging.info("Finishing event {}".format(event))
        event.commit(debriefing)
        if event.is_successfull(debriefing):
            self.budget += event.bonus()

        if event in self.events:
            self.events.remove(event)
        else:
            logging.info("finish_event: event not in the events!")

    def is_player_attack(self, event):
        if isinstance(event, Event):
            return event.attacker_name == self.player
        else:
            return event.name == self.player

    def pass_turn(self, no_action=False, ignored_cps: typing.Collection[ControlPoint]=None):
        logging.info("Pass turn")
        for event in self.events:
            if self.settings.version == "dev":
                # don't damage player CPs in by skipping in dev mode
                if isinstance(event, UnitsDeliveryEvent):
                    event.skip()
            else:
                event.skip()

        for cp in self.theater.enemy_points():
            self._commision_units(cp)
        self._budget_player()

        if not no_action:
            for cp in self.theater.player_points():
                cp.base.affect_strength(+PLAYER_BASE_STRENGTH_RECOVERY)

        self.ignored_cps = []
        if ignored_cps:
            self.ignored_cps = ignored_cps

        self.events = []  # type: typing.List[Event]
        self._generate_events()
        #self._generate_globalinterceptions()

