import typing
import random
from datetime import datetime, timedelta, time

from dcs.mission import Mission
from dcs.triggers import *
from dcs.condition import *
from dcs.action import *
from dcs.unit import Skill
from dcs.point import MovingPoint, PointProperties
from dcs.action import *

from game import db
from theater import *
from gen import *

ACTIVATION_TRIGGER_SIZE = 40000
ACTIVATION_TRIGGER_MIN_DISTANCE = 20000

PUSH_TRIGGER_SIZE = 3000

REGROUP_ZONE_DISTANCE = 12000
REGROUP_ALT = 5000

CLOUDS_BASE_MIN = 4000

RANDOM_TIME = {
    "night": 5,
    "dusk": 30,
    "dawn": 30,
    "day": 100,
}

RANDOM_WEATHER = {
    1: 5,  # heavy rain
    2: 15,  # rain
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
            if self.game.settings.night_disabled and k == "night":
                continue

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

        if self.mission.weather.clouds_density > 0:
            self.mission.weather.clouds_base = max(self.mission.weather.clouds_base, CLOUDS_BASE_MIN)

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

        zone_distance_to_aircraft = self.conflict.from_cp.position.distance_to_point(self.conflict.position)
        zone_size = min(zone_distance_to_aircraft - ACTIVATION_TRIGGER_MIN_DISTANCE, ACTIVATION_TRIGGER_SIZE)

        activation_trigger_zone = self.mission.triggers.add_triggerzone(self.conflict.position, zone_size, name="Activation zone")
        activation_trigger = TriggerOnce(Event.NoEvent, "Activation trigger")
        activation_trigger.add_condition(PartOfCoalitionInZone(player_coalition, activation_trigger_zone.id))
        for group in activate_by_trigger:
            activation_trigger.add_action(ActivateGroup(group.id))

        self.mission.triggerrules.triggers.append(activation_trigger)

    def _gen_push_trigger(self, player_coalition: str):
        push_by_trigger = []
        for coalition_name, coalition in self.mission.coalition.items():
            for country in coalition.countries.values():
                if coalition_name == player_coalition:
                    for plane_group in country.plane_group:
                        if plane_group.task == AWACS.name:
                            continue
                        regroup_heading = self.conflict.to_cp.position.heading_between_point(self.conflict.from_cp.position)

                        pos1 = plane_group.position.point_from_heading(regroup_heading, REGROUP_ZONE_DISTANCE)
                        pos2 = plane_group.position.point_from_heading(regroup_heading, REGROUP_ZONE_DISTANCE+5000)
                        w1 = plane_group.add_waypoint(pos1, REGROUP_ALT)
                        w2 = plane_group.add_waypoint(pos2, REGROUP_ALT)

                        plane_group.points.remove(w1)
                        plane_group.points.remove(w2)

                        plane_group.points.insert(1, w2)
                        plane_group.points.insert(1, w1)

                        w2.tasks.append(SwitchWaypoint(from_waypoint=3, to_waypoint=2))
                        plane_group.add_trigger_action(SwitchWaypoint(to_waypoint=4))
                        push_by_trigger.append(plane_group)

        push_trigger_zone = self.mission.triggers.add_triggerzone(self.conflict.from_cp.position, PUSH_TRIGGER_SIZE, name="Push zone")
        push_trigger = TriggerOnce(Event.NoEvent, "Push trigger")
        push_trigger.add_condition(AllOfCoalitionOutsideZone(player_coalition, push_trigger_zone.id))
        for group in push_by_trigger:
            push_trigger.add_action(AITaskPush(group.id, 1))
        message_string = self.mission.string("Task force is in the air, proceed with the objective.")
        push_trigger.add_action(MessageToAll(message_string, clearview=True))

        self.mission.triggerrules.triggers.append(push_trigger)

    def _set_allegiances(self, player_coalition: str, enemy_coalition: str):
        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)

    def _set_skill(self, player_coalition: str, enemy_coalition: str):
        for coalition_name, coalition in self.mission.coalition.items():
            if coalition_name == player_coalition:
                skill_level = self.game.settings.player_skill
            elif coalition_name == enemy_coalition:
                skill_level = self.game.settings.enemy_skill
            else:
                continue

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
            # TODO: waypoint parts of this should not be post-hacked but added in airgen
            self._gen_activation_trigger(player_coalition, enemy_coalition)
            self._gen_push_trigger(player_coalition)
