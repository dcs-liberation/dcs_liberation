import typing
import random

from dcs.mission import Mission
from dcs.triggers import *
from dcs.condition import *
from dcs.action import *

from theater.weatherforecast import WeatherForecast
from theater.conflicttheater import Conflict

ACTIVATION_TRIGGER_SIZE = 80000
ACTIVATION_TRIGGER_MIN_DISTANCE = 5000

RANDOM_TIME = {
    "night": 0,
    "dusk": 5,
    "dawn": 35,
    "noon": 75,
    "day": 100,
}

RANDOM_WEATHER = {
    0: 0,  #  thunderstorm
    1: 5,  #  heavy rain
    2: 15, #  rain
    3: 35, #  random dynamic
}

class EnvironmentSettingsGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def generate(self, is_quick: bool):
        time_roll = random.randint(0, 100)
        time_period = None
        for k, v in RANDOM_TIME.items():
            if v >= time_roll:
                time_period = k
                break

        self.mission.random_daytime(time_period)

        weather_roll = random.randint(0, 100)
        weather_type = None
        for k, v in RANDOM_TIME.items():
            if v >= weather_roll:
                weather_type = k
                break

        if weather_type == 0:
            self.mission.weather.random_thunderstorm()
        elif weather_type == 1:
            self.mission.weather.heavy_rain()
        elif weather_type == 2:
            self.mission.weather.heavy_rain()
            self.mission.weather.enable_fog = False
        elif weather_type == 3:
            self.mission.weather.random(self.mission.start_time, self.mission.terrain)

        player_coalition = self.game.player == "USA" and "blue" or "red"
        enemy_coalition = player_coalition == "blue" and "red" or "blue"

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)

        if not is_quick:
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
