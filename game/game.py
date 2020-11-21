import logging
import random
import sys
from datetime import date, datetime, timedelta
from typing import Dict, List

from dcs.action import Coalition
from dcs.mapping import Point
from dcs.task import CAP, CAS, PinpointStrike
from dcs.vehicles import AirDefence

from game import db
from game.db import PLAYER_BUDGET_BASE, REWARDS
from game.inventory import GlobalAircraftInventory
from game.models.game_stats import GameStats
from game.plugins import LuaPluginManager
from gen.ato import AirTaskingOrder
from gen.conflictgen import Conflict
from gen.flights.ai_flight_planner import CoalitionMissionPlanner
from gen.flights.closestairfields import ObjectiveDistanceCache
from gen.ground_forces.ai_ground_planner import GroundPlanner
from . import persistency
from .debriefing import Debriefing
from .event.event import Event, UnitsDeliveryEvent
from .event.frontlineattack import FrontlineAttackEvent
from .factions.faction import Faction
from .infos.information import Information
from .settings import Settings
from .theater import ConflictTheater, ControlPoint, OffMapSpawn
from .unitmap import UnitMap
from .weather import Conditions, TimeOfDay

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

# amount of strength player bases recover for the turn
PLAYER_BASE_STRENGTH_RECOVERY = 0.2

# amount of strength enemy bases recover for the turn
ENEMY_BASE_STRENGTH_RECOVERY = 0.05

# cost of AWACS for single operation
AWACS_BUDGET_COST = 4

# Initial budget value
PLAYER_BUDGET_INITIAL = 650

# Bonus multiplier logarithm base
PLAYER_BUDGET_IMPORTANCE_LOG = 2


class Game:
    def __init__(self, player_name: str, enemy_name: str,
                 theater: ConflictTheater, start_date: datetime,
                 settings: Settings):
        self.settings = settings
        self.events: List[Event] = []
        self.theater = theater
        self.player_name = player_name
        self.player_country = db.FACTIONS[player_name].country
        self.enemy_name = enemy_name
        self.enemy_country = db.FACTIONS[enemy_name].country
        self.turn = 0
        self.date = date(start_date.year, start_date.month, start_date.day)
        self.game_stats = GameStats()
        self.game_stats.update(self)
        self.ground_planners: Dict[int, GroundPlanner] = {}
        self.informations = []
        self.informations.append(Information("Game Start", "-" * 40, 0))
        self.__culling_points: List[Point] = []
        self.compute_conflicts_position()
        self.__destroyed_units: List[str] = []
        self.savepath = ""
        self.budget = PLAYER_BUDGET_INITIAL
        self.current_unit_id = 0
        self.current_group_id = 0

        self.conditions = self.generate_conditions()

        self.blue_ato = AirTaskingOrder()
        self.red_ato = AirTaskingOrder()

        self.aircraft_inventory = GlobalAircraftInventory(
            self.theater.controlpoints
        )

        for cp in self.theater.controlpoints:
            cp.pending_unit_deliveries = self.units_delivery_event(cp)

        self.sanitize_sides()
        self.on_load()

    def generate_conditions(self) -> Conditions:
        return Conditions.generate(self.theater, self.date,
                                   self.current_turn_time_of_day, self.settings)

    def sanitize_sides(self):
        """
        Make sure the opposing factions are using different countries
        :return:
        """
        if self.player_country == self.enemy_country:
            if self.player_country == "USA":
                self.enemy_country = "USAF Aggressors"
            elif self.player_country == "Russia":
                self.enemy_country = "USSR"
            else:
                self.enemy_country = "Russia"

    @property
    def player_faction(self) -> Faction:
        return db.FACTIONS[self.player_name]

    @property
    def enemy_faction(self) -> Faction:
        return db.FACTIONS[self.enemy_name]

    def _roll(self, prob, mult):
        if self.settings.version == "dev":
            # always generate all events for dev
            return 100
        else:
            return random.randint(1, 100) <= prob * mult

    def _generate_player_event(self, event_class, player_cp, enemy_cp):
        self.events.append(event_class(self, player_cp, enemy_cp, enemy_cp.position, self.player_name, self.enemy_name))

    def _generate_events(self):
        for front_line in self.theater.conflicts(True):
            self._generate_player_event(FrontlineAttackEvent,
                                        front_line.control_point_a,
                                        front_line.control_point_b)

    @property
    def budget_reward_amount(self):
        reward = 0
        if len(self.theater.player_points()) > 0:
            reward = PLAYER_BUDGET_BASE * len(self.theater.player_points())
            for cp in self.theater.player_points():
                for g in cp.ground_objects:
                    if g.category in REWARDS.keys() and not g.is_dead:
                        reward = reward + REWARDS[g.category]
            return reward
        else:
            return reward

    def _budget_player(self):
        self.budget += self.budget_reward_amount

    def units_delivery_event(self, to_cp: ControlPoint) -> UnitsDeliveryEvent:
        event = UnitsDeliveryEvent(attacker_name=self.player_name,
                                   defender_name=self.player_name,
                                   from_cp=to_cp,
                                   to_cp=to_cp,
                                   game=self)
        self.events.append(event)
        return event

    def initiate_event(self, event: Event) -> UnitMap:
        #assert event in self.events
        logging.info("Generating {} (regular)".format(event))
        return event.generate()

    def finish_event(self, event: Event, debriefing: Debriefing):
        logging.info("Finishing event {}".format(event))
        event.commit(debriefing)
        if event.is_successful(debriefing):
            self.budget += event.bonus()

        if event in self.events:
            self.events.remove(event)
        else:
            logging.info("finish_event: event not in the events!")

    def is_player_attack(self, event):
        if isinstance(event, Event):
            return event and event.attacker_name and event.attacker_name == self.player_name
        else:
            return event and event.name and event.name == self.player_name

    def on_load(self) -> None:
        LuaPluginManager.load_settings(self.settings)
        ObjectiveDistanceCache.set_theater(self.theater)

    def pass_turn(self, no_action: bool = False) -> None:
        logging.info("Pass turn")
        self.informations.append(Information("End of turn #" + str(self.turn), "-" * 40, 0))
        self.turn += 1

        for event in self.events:
            if self.settings.version == "dev":
                # don't damage player CPs in by skipping in dev mode
                if isinstance(event, UnitsDeliveryEvent):
                    event.skip()
            else:
                event.skip()

        self._enemy_reinforcement()
        self._budget_player()

        if not no_action and self.turn > 1:
            for cp in self.theater.player_points():
                cp.base.affect_strength(+PLAYER_BASE_STRENGTH_RECOVERY)
        else:
            for cp in self.theater.player_points():
                if not cp.is_carrier and not cp.is_lha:
                    cp.base.affect_strength(-PLAYER_BASE_STRENGTH_RECOVERY)

        self.conditions = self.generate_conditions()

        self.initialize_turn()

        # Autosave progress
        persistency.autosave(self)

    def initialize_turn(self) -> None:
        self.events = []
        self._generate_events()

        # Update statistics
        self.game_stats.update(self)

        self.aircraft_inventory.reset()
        for cp in self.theater.controlpoints:
            cp.pending_unit_deliveries = self.units_delivery_event(cp)
            self.aircraft_inventory.set_from_control_point(cp)

        # Plan flights & combat for next turn
        self.compute_conflicts_position()
        self.ground_planners = {}
        self.blue_ato.clear()
        self.red_ato.clear()
        CoalitionMissionPlanner(self, is_player=True).plan_missions()
        CoalitionMissionPlanner(self, is_player=False).plan_missions()
        for cp in self.theater.controlpoints:
            if cp.has_frontline:
                gplanner = GroundPlanner(cp, self)
                gplanner.plan_groundwar()
                self.ground_planners[cp.id] = gplanner

    def _enemy_reinforcement(self):
        """
        Compute and commision reinforcement for enemy bases
        """

        MAX_ARMOR = 30 * self.settings.multiplier
        MAX_AIRCRAFT = 25 * self.settings.multiplier

        production = 0.0
        for enemy_point in self.theater.enemy_points():
            for g in enemy_point.ground_objects:
                if g.category in REWARDS.keys() and not g.is_dead:
                    production = production + REWARDS[g.category]

        production = production * 0.75
        budget_for_armored_units = production / 2
        budget_for_aircraft = production / 2

        potential_cp_armor = []
        for cp in self.theater.enemy_points():
            for cpe in cp.connected_points:
                if cpe.captured and cp.base.total_armor < MAX_ARMOR:
                    potential_cp_armor.append(cp)
        if len(potential_cp_armor) == 0:
            potential_cp_armor = self.theater.enemy_points()

        potential_cp_armor = [p for p in potential_cp_armor if
                              not isinstance(p, OffMapSpawn)]

        i = 0
        potential_units = db.FACTIONS[self.enemy_name].frontline_units

        print("Enemy Recruiting")
        print(potential_cp_armor)
        print(budget_for_armored_units)
        print(potential_units)

        if len(potential_units) > 0 and len(potential_cp_armor) > 0:
            while budget_for_armored_units > 0:
                i = i + 1
                if i > 50 or budget_for_armored_units <= 0:
                    break
                target_cp = random.choice(potential_cp_armor)
                if target_cp.base.total_armor >= MAX_ARMOR:
                    continue
                unit = random.choice(potential_units)
                price = db.PRICES[unit] * 2
                budget_for_armored_units -= price * 2
                target_cp.base.armor[unit] = target_cp.base.armor.get(unit, 0) + 2
                info = Information("Enemy Reinforcement", unit.id + " x 2 at " + target_cp.name, self.turn)
                print(str(info))
                self.informations.append(info)

        if budget_for_armored_units > 0:
            budget_for_aircraft += budget_for_armored_units

        potential_units = [u for u in db.FACTIONS[self.enemy_name].aircrafts
                           if u in db.UNIT_BY_TASK[CAS] or u in db.UNIT_BY_TASK[CAP]]

        if len(potential_units) > 0 and len(potential_cp_armor) > 0:
            while budget_for_aircraft > 0:
                i = i + 1
                if i > 50 or budget_for_aircraft <= 0:
                    break
                target_cp = random.choice(potential_cp_armor)
                if target_cp.base.total_aircraft >= MAX_AIRCRAFT:
                    continue
                unit = random.choice(potential_units)
                price = db.PRICES[unit] * 2
                budget_for_aircraft -= price * 2
                target_cp.base.aircraft[unit] = target_cp.base.aircraft.get(unit, 0) + 2
                info = Information("Enemy Reinforcement", unit.id + " x 2 at " + target_cp.name, self.turn)
                print(str(info))
                self.informations.append(info)

    @property
    def current_turn_time_of_day(self) -> TimeOfDay:
        return list(TimeOfDay)[self.turn % 4]

    @property
    def current_day(self) -> date:
        return self.date + timedelta(days=self.turn // 4)

    def next_unit_id(self):
        """
        Next unit id for pre-generated units
        """
        self.current_unit_id += 1
        return self.current_unit_id

    def next_group_id(self):
        """
        Next unit id for pre-generated units
        """
        self.current_group_id += 1
        return self.current_group_id

    def compute_conflicts_position(self):
        """
        Compute the current conflict center position(s), mainly used for culling calculation
        :return: List of points of interests
        """
        points = []

        # By default, use the existing frontline conflict position
        for front_line in self.theater.conflicts():
            position = Conflict.frontline_position(front_line.control_point_a,
                                                   front_line.control_point_b,
                                                   self.theater)
            points.append(position[0])
            points.append(front_line.control_point_a.position)
            points.append(front_line.control_point_b.position)

        # If do_not_cull_carrier is enabled, add carriers as culling point
        if self.settings.perf_do_not_cull_carrier:
            for cp in self.theater.controlpoints:
                if cp.is_carrier or cp.is_lha:
                    points.append(cp.position)

        # If there is no conflict take the center point between the two nearest opposing bases
        if len(points) == 0:
            cpoint = None
            min_distance = sys.maxsize
            for cp in self.theater.player_points():
                for cp2 in self.theater.enemy_points():
                    d = cp.position.distance_to_point(cp2.position)
                    if d < min_distance:
                        min_distance = d
                        cpoint = Point((cp.position.x + cp2.position.x) / 2, (cp.position.y + cp2.position.y) / 2)
                        points.append(cp.position)
                        points.append(cp2.position)
                        break
                if cpoint is not None:
                    break
            if cpoint is not None:
                points.append(cpoint)

        # Else 0,0, since we need a default value
        # (in this case this means the whole map is owned by the same player, so it is not an issue)
        if len(points) == 0:
            points.append(Point(0, 0))

        self.__culling_points = points

    def add_destroyed_units(self, data):
        pos = Point(data["x"], data["z"])
        if self.theater.is_on_land(pos):
            self.__destroyed_units.append(data)

    def get_destroyed_units(self):
        return self.__destroyed_units

    def position_culled(self, pos):
        """
        Check if unit can be generated at given position depending on culling performance settings
        :param pos: Position you are tryng to spawn stuff at
        :return: True if units can not be added at given position
        """
        if self.settings.perf_culling == False:
            return False
        else:
            for c in self.__culling_points:
                if c.distance_to_point(pos) < self.settings.perf_culling_distance * 1000:
                    return False
            return True

    def get_culling_points(self):
        """
        Check culling points
        :return: List of culling points
        """
        return self.__culling_points

    # 1 = red, 2 = blue
    def get_player_coalition_id(self):
        return 2

    def get_enemy_coalition_id(self):
        return 1

    def get_player_coalition(self):
        return Coalition.Blue

    def get_enemy_coalition(self):
        return Coalition.Red

    def get_player_color(self):
        return "blue"

    def get_enemy_color(self):
        return "red"