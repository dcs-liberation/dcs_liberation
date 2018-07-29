import logging
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
from dcs.weather import *

from game import db
from theater import *
from gen import *

WEATHER_CLOUD_BASE = 2000, 3000
WEATHER_CLOUD_DENSITY = 1, 8
WEATHER_CLOUD_THICKNESS = 100, 400
WEATHER_CLOUD_BASE_MIN = 1600

RANDOM_TIME = {
    "night": 5,
    "dusk": 30,
    "dawn": 30,
    "day": 100,
}

RANDOM_WEATHER = {
    1: 0,  # heavy rain
    2: 10,  # rain
    3: 20,  # dynamic
    4: 30,  # clear
    5: 100,  # random
}


class EnvironmentSettings:
    weather_dict = None
    start_time = None


class EnviromentGenerator:
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

        logging.info("generated weather {}".format(weather_type))
        if weather_type == 1:
            self.mission.weather.heavy_rain()
        elif weather_type == 2:
            self.mission.weather.heavy_rain()
            self.mission.weather.enable_fog = False
        elif weather_type == 3:
            self.mission.weather.random(self.mission.start_time, self.conflict.theater.terrain)
        elif weather_type == 4:
            pass
        elif weather_type == 5:
            self.mission.weather.clouds_base = random.randint(*WEATHER_CLOUD_BASE)
            self.mission.weather.clouds_density = random.randint(*WEATHER_CLOUD_DENSITY)
            self.mission.weather.clouds_thickness = random.randint(*WEATHER_CLOUD_THICKNESS)

            wind_direction = random.randint(0, 360)
            wind_speed = random.randint(0, 13)
            self.mission.weather.wind_at_ground = Wind(wind_direction, wind_speed)
            self.mission.weather.wind_at_2000 = Wind(wind_direction, wind_speed * 2)
            self.mission.weather.wind_at_8000 = Wind(wind_direction, wind_speed * 3)

        if self.mission.weather.clouds_density > 0:
            # sometimes clouds are randomized way too low and need to be fixed
            self.mission.weather.clouds_base = max(self.mission.weather.clouds_base, WEATHER_CLOUD_BASE_MIN)

        if self.mission.weather.wind_at_ground == 0:
            # frontline smokes look silly w/o any wind
            self.mission.weather.wind_at_ground = random.randint(1, 2)

    def generate(self) -> EnvironmentSettings:
        self._gen_random_time()
        self._gen_random_weather()

        settings = EnvironmentSettings()
        settings.start_time = self.mission.start_time
        settings.weather_dict = self.mission.weather.dict()
        return settings

    def load(self, settings: EnvironmentSettings):
        self.mission.start_time = settings.start_time
        self.mission.weather.load_from_dict(settings.weather_dict)

