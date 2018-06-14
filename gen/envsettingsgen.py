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
        self.mission.weather.random(self.mission.start_time, self.mission.terrain)

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue

            player_coalition = self.game.player == "USA" and "blue" or "red"
            enemy_coalition = player_coalition == "blue" and "red" or "blue"
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)
