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
from game.utils import Distance, meters, interpolate

if TYPE_CHECKING:
    from game.theater import ConflictTheater


class TimeOfDay(Enum):
    Dawn = "dawn"
    Day = "day"
    Dusk = "dusk"
    Night = "night"


# NOTES FROM ATC GUY
# 30.12 typical summer high pressure (nordics)
# 29.68 lower bound typical summer rain (nordics)
# conclusion: add/subtract 0.22 for clear vs rain
# 27.91 crazy low, seen
# 31.30 crazy high, seen
# Thunderstorm keeps pressure high
# conclusion: add 0.22 for thunderstorm
# Pressure doesn't change much during night
# Seasonal variations are smaller close to the equator

@dataclass(frozen=True)
class AtmosphericConditions:
    #: Pressure at sea level in inches of mercury.
    qnh_inches_mercury: float
    #: Temperature at sea level in Celcius.
    temperature_celsius: float


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
    def __init__(self, seasonal_conditions: SeasonalConditions, day: datetime.date, time_of_day: TimeOfDay) -> None:
        # Future improvement: Use theater, day and time of day
        # to get a more realistic conditions
        self.atmospheric = self.generate_atmospheric(seasonalConditions, day, time_of_day)
        self.clouds = self.generate_clouds()
        self.fog = self.generate_fog()
        self.wind = self.generate_wind()

    def generate_atmospheric(self, seasonal_conditions: SeasonalConditions, day: datetime.date, time_of_day: TimeOfDay) -> AtmosphericConditions:
        pressure = self.interpolate_summer_winter(seasonal_conditions.summer_avg_pressure, seasonal_conditions.winter_avg_pressure, day)
        print("!!! pressure!", pressure)
        temperature = self.interpolate_summer_winter(seasonal_conditions.summer_avg_temperature, seasonal_conditions.winter_avg_temperature, day)
        print("!!! temperature!", temperature)
        if time_of_day == TimeOfDay.Day:
            print("!!! is day")
            temperature += seasonal_conditions.temperature_day_night_difference / 2
        if time_of_day == TimeOfDay.Night:
            print("!!! is night!")
            temperature -= seasonal_conditions.temperature_day_night_difference / 2
        pressure_adjustment = self.get_pressure_adjustment()
        temperature_adjustment = self.get_temperature_adjustment()
        return AtmosphericConditions(
            qnh_inches_mercury=self.random_pressure(pressure + pressure_adjustment),
            temperature_celsius=self.random_temperature(temperature + temperature_adjustment),
        )

    def get_pressure_adjustment(self) -> float:
        raise NotImplementedError
    
    def get_temperature_adjustment(self) -> float:
        raise NotImplementedError

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

    @staticmethod
    def random_pressure(average_pressure: float) -> float:
        # "Safe" constants based roughly on ME and viper altimeter.
        # Units are inches of mercury.
        SAFE_MIN = 28.4
        SAFE_MAX = 30.9
        # Use normalvariate to get normal distribution, more realistic than uniform
        pressure = random.normalvariate(average_pressure, 0.2)
        return max(SAFE_MIN, min(SAFE_MAX, pressure))

    @staticmethod
    def random_temperature(average_temperature: float) -> float:
        # "Safe" constants based roughly on ME.
        # Temperatures are in Celcius.
        SAFE_MIN = -12
        SAFE_MAX = 49
        # Use normalvariate to get normal distribution, more realistic than uniform
        temperature = random.normalvariate(average_temperature, 4)
        temperature = round(temperature)
        return max(SAFE_MIN, min(SAFE_MAX, temperature))

    @staticmethod
    def interpolate_summer_winter(summer_value: float, winter_value: float, day: datetime.date) -> float:
        day_of_year = day.timetuple().tm_yday
        day_of_year_peak_summer = 183
        distance_from_peak_summer = abs(-day_of_year_peak_summer + day_of_year)
        winter_factor = distance_from_peak_summer / day_of_year_peak_summer
        return interpolate(summer_value, winter_value, winter_factor, clamp=True)

    # TODO: Day/night interpolation
    


class ClearSkies(Weather):
    def get_pressure_adjustment(self) -> float:
        return 0.22

    def get_temperature_adjustment(self) -> float:
        return 3.0

    def generate_clouds(self) -> Optional[Clouds]:
        return None

    def generate_fog(self) -> Optional[Fog]:
        return None

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 0)


class Cloudy(Weather):
    def get_pressure_adjustment(self) -> float:
        return 0.0

    def get_temperature_adjustment(self) -> float:
        return 0.0

    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds.random_preset(rain=False)

    def generate_fog(self) -> Optional[Fog]:
        # DCS 2.7 says to not use fog with the cloud presets.
        return None

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 4)


class Raining(Weather):
    def get_pressure_adjustment(self) -> float:
        return -0.22

    def get_temperature_adjustment(self) -> float:
        return -3.0

    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds.random_preset(rain=True)

    def generate_fog(self) -> Optional[Fog]:
        # DCS 2.7 says to not use fog with the cloud presets.
        return None

    def generate_wind(self) -> WindConditions:
        return self.random_wind(0, 6)


class Thunderstorm(Weather):
    def get_pressure_adjustment(self) -> float:
        return 0.1

    def get_temperature_adjustment(self) -> float:
        return -3.0

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
        _start_time = cls.generate_start_time(
            theater, day, time_of_day, settings.night_disabled
        )
        return cls(
            time_of_day=time_of_day,
            start_time=_start_time,
            weather=cls.generate_weather(theater.seasonal_conditions, day, time_of_day),
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
    def generate_weather(cls, seasonal_conditions: SeasonalConditions, day: datetime.date, time_of_day: TimeOfDay) -> Weather:
        # Here we could hook in seasonal weights
        chances = {
            Thunderstorm: 1,
            Raining: 20,
            Cloudy: 60,
            ClearSkies: 20,
        }
        weather_type = random.choices(
            list(chances.keys()), weights=list(chances.values())
        )[0]
        return weather_type(seasonal_conditions, day, time_of_day)
