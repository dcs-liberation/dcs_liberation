import typing
import random
from datetime import datetime, timedelta, time

from dcs.mission import Mission
from dcs.triggers import *
from dcs.condition import *
from dcs.action import *
from dcs.unit import Skill

from game import db
from theater import *
from gen import *

ACTIVATION_TRIGGER_SIZE = 40000
ACTIVATION_TRIGGER_MIN_DISTANCE = 5000

RANDOM_TIME = {
    "night": 5,
    "dusk": 30,
    "dawn": 30,
    "day": 100,
}

RANDOM_WEATHER = {
    1: 10,  # heavy rain
    2: 20,  # rain
    3: 100,  # random dynamic
}


class SettingsGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def _gen_random_time(self):
        start_time = datetime.combine(datetime.today(), time())
        time_range = None
        for k, v in RANDOM_TIME.items():
            if random.randint(0, 100) <= v:
                time_range = self.game.theater.daytime_map[k]
                break

        start_time += timedelta(hours=random.randint(*time_range))
        self.mission.start_time = start_time

    def _gen_random_weather(self):
        weather_type = None
        for k, v in RANDOM_WEATHER.items():
            if random.randint(0, 100) <= v:
                weather_type = k
                break

        print("generated weather {}".format(weather_type))
        if weather_type == 0:
            self.mission.weather.random_thunderstorm()
        elif weather_type == 1:
            self.mission.weather.heavy_rain()
        elif weather_type == 2:
            self.mission.weather.heavy_rain()
            self.mission.weather.enable_fog = False
        elif weather_type == 3:
            pass

    def _gen_activation_trigger(self, player_coalition: str, enemy_coalition: str):
        activate_by_trigger = []
        for coalition_name, coalition in self.mission.coalition.items():
            for country in coalition.countries.values():
                if coalition_name == enemy_coalition:
                    for plane_group in country.plane_group:
                        plane_group.late_activation = True
                        activate_by_trigger.append(plane_group)

                for vehicle_group in country.vehicle_group:
                    vehicle_group.late_activation = True
                    activate_by_trigger.append(vehicle_group)

        zone_distance_to_aircraft = self.conflict.air_attackers_location.distance_to_point(self.conflict.position)
        zone_size = min(zone_distance_to_aircraft - ACTIVATION_TRIGGER_MIN_DISTANCE, ACTIVATION_TRIGGER_SIZE)

        activation_trigger_zone = self.mission.triggers.add_triggerzone(self.conflict.position, zone_size)
        activation_trigger = TriggerOnce(Event.NoEvent, "Activation trigger")
        activation_trigger.add_condition(PartOfCoalitionInZone(player_coalition, activation_trigger_zone.id))
        for group in activate_by_trigger:
            activation_trigger.add_action(ActivateGroup(group.id))

        self.mission.triggerrules.triggers.append(activation_trigger)

    def _set_allegiances(self, player_coalition: str, enemy_coalition: str):
        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)

    def _set_skill(self, player_coalition: str, enemy_coalition: str):
        for coalition_name, coalition in self.mission.coalition.items():
            skill_level = player_coalition == coalition_name and self.game.player_skill or self.game.enemy_skill
            for country in coalition.countries.values():
                for plane_group in country.plane_group:
                    for plane_unit in plane_group.units:
                        if plane_unit.skill != Skill.Client and plane_unit.skill != Skill.Player:
                            plane_unit.skill = Skill(skill_level)

                for vehicle_group in country.vehicle_group:
                    vehicle_group.set_skill(Skill(skill_level))

    def generate(self, is_quick: bool):
        player_coalition = self.game.player == "USA" and "blue" or "red"
        enemy_coalition = player_coalition == "blue" and "red" or "blue"

        self.mission.coalition[player_coalition].bullseye = {"x": self.conflict.position.x,
                                                             "y": self.conflict.position.y}

        self._gen_random_time()
        self._gen_random_weather()
        self._set_skill(player_coalition, enemy_coalition)
        self._set_allegiances(player_coalition, enemy_coalition)

        if not is_quick:
            self._gen_activation_trigger(player_coalition, enemy_coalition)
