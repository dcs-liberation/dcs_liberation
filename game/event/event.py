import typing
import logging

from dcs.action import Coalition
from dcs.unittype import UnitType
from dcs.task import *
from dcs.vehicles import AirDefence
from dcs.unittype import UnitType

from game import *
from theater import *
from gen.environmentgen import EnvironmentSettings
from gen.conflictgen import Conflict
from game.db import assigned_units_from, unitdict_from

from userdata.debriefing import Debriefing
from userdata import persistency

import game.db as db

DIFFICULTY_LOG_BASE = 1.1
EVENT_DEPARTURE_MAX_DISTANCE = 340000


MINOR_DEFEAT_INFLUENCE = 0.1
DEFEAT_INFLUENCE = 0.3
STRONG_DEFEAT_INFLUENCE = 0.5

class Event:
    silent = False
    informational = False
    is_awacs_enabled = False
    ca_slots = 0

    game = None  # type: Game
    location = None  # type: Point
    from_cp = None  # type: ControlPoint
    departure_cp = None  # type: ControlPoint
    to_cp = None  # type: ControlPoint

    operation = None  # type: Operation
    difficulty = 1  # type: int
    environment_settings = None  # type: EnvironmentSettings
    BONUS_BASE = 5

    def __init__(self, game, from_cp: ControlPoint, target_cp: ControlPoint, location: Point, attacker_name: str, defender_name: str):
        self.game = game
        self.departure_cp = None
        self.from_cp = from_cp
        self.to_cp = target_cp
        self.location = location
        self.attacker_name = attacker_name
        self.defender_name = defender_name

    @property
    def is_player_attacking(self) -> bool:
        return self.attacker_name == self.game.player_name

    @property
    def enemy_cp(self) -> ControlPoint:
        if self.attacker_name == self.game.player_name:
            return self.to_cp
        else:
            return self.departure_cp

    @property
    def threat_description(self) -> str:
        return ""

    def flight_name(self, for_task: typing.Type[typing.Type[Task]]) -> str:
        return "Flight"

    @property
    def tasks(self) -> typing.Collection[typing.Type[Task]]:
        return []

    @property
    def ai_banned_tasks(self) -> typing.Collection[typing.Type[Task]]:
        return []

    @property
    def player_banned_tasks(self) -> typing.Collection[typing.Type[Task]]:
        return []

    @property
    def global_cp_available(self) -> bool:
        return False

    def is_departure_available_from(self, cp: ControlPoint) -> bool:
        if not cp.captured:
            return False

        if self.location.distance_to_point(cp.position) > EVENT_DEPARTURE_MAX_DISTANCE:
            return False

        if cp.is_global and not self.global_cp_available:
            return False

        return True

    def bonus(self) -> int:
        return int(math.log(self.to_cp.importance + 1, DIFFICULTY_LOG_BASE) * self.BONUS_BASE)

    def is_successfull(self, debriefing: Debriefing) -> bool:
        return self.operation.is_successfull(debriefing)

    def player_attacking(self, cp: ControlPoint, flights: db.TaskForceDict):
        if self.is_player_attacking:
            self.departure_cp = cp
        else:
            self.to_cp = cp

    def player_defending(self, cp: ControlPoint, flights: db.TaskForceDict):
        if self.is_player_attacking:
            self.departure_cp = cp
        else:
            self.to_cp = cp

    def generate(self):
        self.operation.is_awacs_enabled = self.is_awacs_enabled
        self.operation.ca_slots = self.ca_slots

        self.operation.prepare(self.game.theater.terrain, is_quick=False)
        self.operation.generate()
        self.operation.current_mission.save(persistency.mission_path_for("liberation_nextturn.miz"))
        self.environment_settings = self.operation.environment_settings

    def generate_quick(self):
        pass
        # TODO : This is not needed anymore. The player can start mission in flight from the flight planner if he want it to be quick.
        # TODO : remove this method
        #self.operation.is_awacs_enabled = self.is_awacs_enabled
        #self.operation.environment_settings = self.environment_settings
        #
        #self.operation.prepare(self.game.theater.terrain, is_quick=True)
        #self.operation.generate()
        #self.operation.current_mission.save(persistency.mission_path_for("liberation_nextturn_quick.miz"))

    def commit(self, debriefing: Debriefing):

        logging.info("Commiting mission results")

        # ------------------------------
        # Destroyed aircrafts
        cp_map = {cp.id: cp for cp in self.game.theater.controlpoints}
        for destroyed_aircraft in debriefing.killed_aircrafts:
            try:
                cpid = int(destroyed_aircraft.split("|")[3])
                type = db.unit_type_from_name(destroyed_aircraft.split("|")[4])
                if cpid in cp_map.keys():
                    cp = cp_map[cpid]
                    if type in cp.base.aircraft.keys():
                        logging.info("Aircraft destroyed : " + str(type))
                        cp.base.aircraft[type] = max(0, cp.base.aircraft[type]-1)
            except Exception as e:
                print(e)

        # ------------------------------
        # Destroyed ground units
        killed_unit_count_by_cp = {cp.id: 0 for cp in self.game.theater.controlpoints}
        cp_map = {cp.id: cp for cp in self.game.theater.controlpoints}
        for killed_ground_unit in debriefing.killed_ground_units:
            try:
                cpid = int(killed_ground_unit.split("|")[3])
                type = db.unit_type_from_name(killed_ground_unit.split("|")[4])
                if cpid in cp_map.keys():
                    killed_unit_count_by_cp[cpid] = killed_unit_count_by_cp[cpid] + 1
                    cp = cp_map[cpid]
                    if type in cp.base.armor.keys():
                        logging.info("Ground unit destroyed : " + str(type))
                        cp.base.armor[type] = max(0, cp.base.armor[type] - 1)
            except Exception as e:
                print(e)

        # ------------------------------
        # Static ground objects
        for destroyed_ground_unit_name in debriefing.killed_ground_units:
            for cp in self.game.theater.controlpoints:
                if not cp.ground_objects:
                    continue

                # -- Static ground objects
                for i, ground_object in enumerate(cp.ground_objects):
                    if ground_object.is_dead:
                        continue

                    if ground_object.matches_string_identifier(destroyed_ground_unit_name):
                        logging.info("cp {} killing ground object {}".format(cp, ground_object.string_identifier))
                        cp.ground_objects[i].is_dead = True

                # -- AA Site groups
                for i, ground_object in enumerate(cp.ground_objects):
                    if ground_object.dcs_identifier in ["AA", "CARRIER", "LHA"]:
                        for g in ground_object.groups:
                            for u in g.units:
                                if u.name == destroyed_ground_unit_name:
                                    g.units.remove(u)
                        ucount = sum([len(g.units) for g in ground_object.groups])
                        if ucount == 0:
                            ground_object.is_dead = True

        # ------------------------------
        # Captured bases
        if self.game.player_country in db.BLUEFOR_FACTIONS:
            coalition = 2 # Value in DCS mission event for BLUE
        else:
            coalition = 1 # Value in DCS mission event for RED

        for captured in debriefing.base_capture_events:
            try:
                id = int(captured.split("||")[0])
                new_owner_coalition = int(captured.split("||")[1])

                for cp in self.game.theater.controlpoints:
                    if cp.id == id:
                        if cp.captured and new_owner_coalition != coalition:
                            cp.captured = False
                            cp.base.aircraft = {}
                            cp.base.armor = {}
                            cp.base.aa = {}
                            for g in cp.ground_objects:
                                g.groups = []
                        elif not(cp.captured) and new_owner_coalition == coalition:
                            cp.captured = True
                            cp.base.aircraft = {}
                            cp.base.armor = {}
                            cp.base.aa = {}
                            for g in cp.ground_objects:
                                g.groups = []
            except Exception as e:
                print(e)

        # -----------------------------------
        # Compute damage to bases
        for cp in self.game.theater.player_points():
            enemy_cps = [e for e in cp.connected_points if not e.captured]
            for enemy_cp in enemy_cps:
                print("Compute frontline progression for : " + cp.name + " to " + enemy_cp.name)

                delta = 0
                player_won = True
                ally_casualties = killed_unit_count_by_cp[cp.id]
                enemy_casualties = killed_unit_count_by_cp[enemy_cp.id]
                ally_units_alive = cp.base.total_armor
                enemy_units_alive = enemy_cp.base.total_armor

                print(ally_units_alive)
                print(enemy_units_alive)
                print(ally_casualties)
                print(enemy_casualties)

                ratio = (1.0 + enemy_casualties) / (1.0 + ally_casualties)

                if ally_units_alive == 0:
                    player_won = False
                    delta = STRONG_DEFEAT_INFLUENCE
                elif enemy_units_alive == 0:
                    player_won = True
                    delta = STRONG_DEFEAT_INFLUENCE
                elif cp.stances[enemy_cp.id] == CombatStance.RETREAT:
                    player_won = False
                    delta = STRONG_DEFEAT_INFLUENCE
                else:
                    if enemy_casualties > ally_casualties:
                        player_won = True
                        if cp.stances[enemy_cp.id] == CombatStance.BREAKTHROUGH:
                            delta = STRONG_DEFEAT_INFLUENCE
                        else:
                            if ratio > 3:
                                delta = STRONG_DEFEAT_INFLUENCE
                            elif ratio < 1.5:
                                delta = MINOR_DEFEAT_INFLUENCE
                            else:
                                delta = DEFEAT_INFLUENCE
                    elif ally_casualties > enemy_casualties:
                        player_won = False
                        if cp.stances[enemy_cp.id] == CombatStance.BREAKTHROUGH:
                            delta = STRONG_DEFEAT_INFLUENCE
                        else:
                            delta = STRONG_DEFEAT_INFLUENCE

                    # No progress with defensive strategies
                    if player_won and cp.stances[enemy_cp.id] in [CombatStance.DEFENSIVE, CombatStance.AMBUSH]:
                        print("Defensive stance, no progress")
                        delta = 0

                if player_won:
                    print(cp.name + " won !  factor > " + str(delta))
                    cp.base.affect_strength(delta)
                    enemy_cp.base.affect_strength(-delta)
                else:
                    print(enemy_cp.name + " won ! factor > " + str(delta))
                    enemy_cp.base.affect_strength(delta)
                    cp.base.affect_strength(-delta)

    def skip(self):
        pass


class UnitsDeliveryEvent(Event):
    informational = True
    units = None  # type: typing.Dict[UnitType, int]

    def __init__(self, attacker_name: str, defender_name: str, from_cp: ControlPoint, to_cp: ControlPoint, game):
        super(UnitsDeliveryEvent, self).__init__(game=game,
                                                 location=to_cp.position,
                                                 from_cp=from_cp,
                                                 target_cp=to_cp,
                                                 attacker_name=attacker_name,
                                                 defender_name=defender_name)

        self.units = {}

    def __str__(self):
        return "Pending delivery to {}".format(self.to_cp)

    def deliver(self, units: typing.Dict[UnitType, int]):
        for k, v in units.items():
            self.units[k] = self.units.get(k, 0) + v

    def skip(self):
        self.to_cp.base.commision_units(self.units)
