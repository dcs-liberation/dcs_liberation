import typing
import logging

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

DIFFICULTY_LOG_BASE = 1.1


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
        return self.attacker_name == self.game.player

    @property
    def enemy_cp(self) -> ControlPoint:
        if self.attacker_name == self.game.player:
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
    def global_cp_available(self) -> bool:
        return False

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
        self.operation.is_awacs_enabled = self.is_awacs_enabled
        self.operation.environment_settings = self.environment_settings

        self.operation.prepare(self.game.theater.terrain, is_quick=True)
        self.operation.generate()
        self.operation.current_mission.save(persistency.mission_path_for("liberation_nextturn_quick.miz"))

    def commit(self, debriefing: Debriefing):
        for country, losses in debriefing.destroyed_units.items():
            if country == self.attacker_name:
                cp = self.departure_cp
            else:
                cp = self.to_cp

            logging.info("base {} commit losses {}".format(cp.base, losses))
            cp.base.commit_losses(losses)

        for object_identifier in debriefing.destroyed_objects:
            for cp in self.game.theater.controlpoints:
                if not cp.ground_objects:
                    continue

                for i, ground_object in enumerate(cp.ground_objects):
                    if ground_object.is_dead:
                        continue

                    if ground_object.matches_string_identifier(object_identifier):
                        logging.info("cp {} killing ground object {}".format(cp, ground_object.string_identifier))
                        cp.ground_objects[i].is_dead = True

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
