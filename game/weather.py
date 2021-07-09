from __future__ import annotations

import datetime
import logging
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, TYPE_CHECKING

from dcs.cloud_presets import Clouds as PydcsClouds
from dcs.weather import CloudPreset, Weather as PydcsWeather, Wind

from game.settings import Settings
from game.utils import Distance, meters

if TYPE_CHECKING:
    from game.theater import ConflictTheater


class TimeOfDay(Enum):
    Dawn = "dawn"
    Day = "day"
    Dusk = "dusk"
    Night = "night"


@dataclass(frozen=True)
class WindConditions:
    at_0m: Wind
    at_2000m: Wind
    at_8000m: Wind


@dataclass(frozen=True)
class Clouds:
    base: int
    density: int
    thickness: int
    precipitation: PydcsWeather.Preceptions
    preset: Optional[CloudPreset] = field(default=None)

    @classmethod
    def random_preset(cls, rain: bool) -> Clouds:
        clouds = (p.value for p in PydcsClouds)
        if rain:
            presets = [p for p in clouds if "Rain" in p.name]
        else:
            presets = [p for p in clouds if "Rain" not in p.name]
        preset = random.choice(presets)
        return Clouds(
            base=random.randint(preset.min_base, preset.max_base),
            density=0,
            thickness=0,
            precipitation=PydcsWeather.Preceptions.None_,
            preset=preset,
        )


@dataclass(frozen=True)
class Fog:
    visibility: Distance
    thickness: int


class Weather:
    def __init__(self) -> None:
        self.clouds = self.generate_clouds()
        self.fog = self.generate_fog()
        self.wind = self.generate_wind()

    def generate_clouds(self) -> Optional[Clouds]:
        raise NotImplementedError

    def generate_fog(self) -> Optional[Fog]:
        if random.randrange(5) != 0:
            return None
        return Fog(
            visibility=meters(random.randint(2500, 5000)),
            thickness=random.randint(100, 500),
        )

    def generate_wind(self) -> WindConditions:
        raise NotImplementedError

    @staticmethod
    def random_wind(minimum: int, maximum: int) -> WindConditions:
        wind_direction = random.randint(0, 360)
        at_0m_factor = 1
        at_2000m_factor = 2
        at_8000m_factor = 3
        base_wind = random.randint(minimum, maximum)

        return WindConditions(
            # Always some wind to make the smoke move a bit.
            at_0m=Wind(wind_direction, max(1, base_wind * at_0m_factor)),
            at_2000m=Wind(wind_direction, base_wind * at_2000m_factor),
            at_8000m=Wind(wind_direction, base_wind * at_8000m_factor),
        )

    @staticmethod
    def random_cloud_base() -> int:
        return random.randint(2000, 3000)

    @staticmethod
    def random_cloud_thickness() -> int:
        return random.randint(100, 400)


class ClearSkies(Weather):
    def generate_clouds(self) -> Optional[Clouds]:
        return None

    def generate_fog(self) -> Optional[Fog]:
        return None

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 0)


class Cloudy(Weather):
    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds.random_preset(rain=False)

    def generate_fog(self) -> Optional[Fog]:
        # DCS 2.7 says to not use fog with the cloud presets.
        return None

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 4)


class Raining(Weather):
    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds.random_preset(rain=True)

    def generate_fog(self) -> Optional[Fog]:
        # DCS 2.7 says to not use fog with the cloud presets.
        return None

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 6)


class Thunderstorm(Weather):
    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds(
            base=self.random_cloud_base(),
            density=random.randint(9, 10),
            thickness=self.random_cloud_thickness(),
            precipitation=PydcsWeather.Preceptions.Thunderstorm,
        )

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 8)


@dataclass
class Conditions:
    time_of_day: TimeOfDay
    start_time: datetime.datetime
    weather: Weather

    @classmethod
    def generate(
        cls,
        theater: ConflictTheater,
        day: datetime.date,
        time_of_day: TimeOfDay,
        settings: Settings,
    ) -> Conditions:
        return cls(
            time_of_day=time_of_day,
            start_time=cls.generate_start_time(
                theater, day, time_of_day, settings.night_disabled
            ),
            weather=cls.generate_weather(),
        )

    @classmethod
    def generate_start_time(
        cls,
        theater: ConflictTheater,
        day: datetime.date,
        time_of_day: TimeOfDay,
        night_disabled: bool,
    ) -> datetime.datetime:
        if night_disabled:
            logging.info("Skip Night mission due to user settings")
            time_range = {
                TimeOfDay.Dawn: (8, 9),
                TimeOfDay.Day: (10, 12),
                TimeOfDay.Dusk: (12, 14),
                TimeOfDay.Night: (14, 17),
            }[time_of_day]
        else:
            time_range = theater.daytime_map[time_of_day.value]

        time = datetime.time(hour=random.randint(*time_range))
        return datetime.datetime.combine(day, time)

    @classmethod
    def generate_weather(cls) -> Weather:
        chances = {
            Thunderstorm: 1,
            Raining: 20,
            Cloudy: 60,
            ClearSkies: 20,
        }
        weather_type = random.choices(
            list(chances.keys()), weights=list(chances.values())
        )[0]
        return weather_type()
