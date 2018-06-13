import typing
import random

from dcs.mission import Mission

from theater.weatherforecast import WeatherForecast


RANDOM_TIME = {
    "night": 5,
    "dusk": 25,
    "down": 50,
    "noon": 75,
    "day": 100,
}


class EnvironmentSettingsGenerator:
    def __init__(self, mission: Mission):
        self.mission = mission

    def generate(self):
        self.mission.random_weather = True

        time_roll = random.randint(0, 100)
        time_period = [k for k, v in RANDOM_TIME.items() if v > time_roll][-1]
        self.mission.random_daytime(time_period)

