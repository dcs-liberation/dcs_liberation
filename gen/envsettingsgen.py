import typing
import random

from dcs.mission import Mission

from theater.weatherforecast import WeatherForecast


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
    def __init__(self, mission: Mission, game):
        self.mission = mission
        self.game = game

    def generate(self):
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

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue

            player_coalition = self.game.player == "USA" and "blue" or "red"
            enemy_coalition = player_coalition == "blue" and "red" or "blue"
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)
