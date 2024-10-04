from __future__ import annotations

import datetime
import logging
import math
import random
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from dcs.weather import Weather as PydcsWeather

from game.timeofday import TimeOfDay
from game.utils import (
    Pressure,
    inches_hg,
    interpolate,
    meters,
)
from game.weather.atmosphericconditions import AtmosphericConditions
from game.weather.clouds import Clouds
from game.weather.fog import Fog
from game.weather.weatherarchetype import WeatherArchetype, WeatherArchetypes
from game.weather.wind import WindConditions

if TYPE_CHECKING:
    from game.theater.seasonalconditions import SeasonalConditions


class Weather(ABC):
    def __init__(
        self,
        seasonal_conditions: SeasonalConditions,
        day: datetime.date,
        time_of_day: TimeOfDay,
    ) -> None:
        # Future improvement: Use theater, day and time of day
        # to get a more realistic conditions
        self.atmospheric = self.generate_atmospheric(
            seasonal_conditions, day, time_of_day
        )
        self.clouds = self.generate_clouds()
        self.fog = self.generate_fog()
        self.wind = self.generate_wind()

    def generate_atmospheric(
        self,
        seasonal_conditions: SeasonalConditions,
        day: datetime.date,
        time_of_day: TimeOfDay,
    ) -> AtmosphericConditions:
        pressure = self.interpolate_summer_winter(
            seasonal_conditions.summer_avg_pressure,
            seasonal_conditions.winter_avg_pressure,
            day,
        )
        temperature = self.interpolate_summer_winter(
            seasonal_conditions.summer_avg_temperature,
            seasonal_conditions.winter_avg_temperature,
            day,
        )

        seasonal_turbulence = self.interpolate_seasonal_turbulence(
            seasonal_conditions.high_avg_yearly_turbulence_per_10cm,
            seasonal_conditions.low_avg_yearly_turbulence_per_10cm,
            day,
        )

        day_turbulence = seasonal_conditions.solar_noon_turbulence_per_10cm
        night_turbulence = seasonal_conditions.midnight_turbulence_per_10cm
        time_of_day_turbulence = self.interpolate_solar_activity(
            time_of_day, day_turbulence, night_turbulence
        )

        random_turbulence = random.normalvariate(mu=0, sigma=0.5)

        turbulence = abs(
            seasonal_turbulence + time_of_day_turbulence + random_turbulence
        )

        if time_of_day == TimeOfDay.Day:
            temperature += seasonal_conditions.temperature_day_night_difference / 2
        if time_of_day == TimeOfDay.Night:
            temperature -= seasonal_conditions.temperature_day_night_difference / 2
        pressure += self.pressure_adjustment
        temperature += self.temperature_adjustment
        turbulence += self.turbulence_adjustment
        logging.debug(
            "Weather: Before random: temp {} press {}".format(temperature, pressure)
        )
        conditions = AtmosphericConditions(
            qnh=self.random_pressure(pressure),
            temperature_celsius=self.random_temperature(temperature),
            turbulence_per_10cm=turbulence,
        )
        logging.debug(
            "Weather: After random: temp {} press {}".format(
                conditions.temperature_celsius, conditions.qnh.pressure_in_inches_hg
            )
        )
        return conditions

    @property
    @abstractmethod
    def archetype(self) -> WeatherArchetype: ...

    @property
    def pressure_adjustment(self) -> float:
        raise NotImplementedError

    @property
    def temperature_adjustment(self) -> float:
        raise NotImplementedError

    @property
    def turbulence_adjustment(self) -> float:
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
        return self.archetype.wind_parameters.speed.random_wind()

    @staticmethod
    def random_cloud_base() -> int:
        return random.randint(2000, 3000)

    @staticmethod
    def random_cloud_thickness() -> int:
        return random.randint(100, 400)

    @staticmethod
    def random_pressure(average_pressure: float) -> Pressure:
        # "Safe" constants based roughly on ME and viper altimeter.
        # Units are inches of mercury.
        SAFE_MIN = 28.4
        SAFE_MAX = 30.9
        # Use normalvariate to get normal distribution, more realistic than uniform
        pressure = random.normalvariate(average_pressure, 0.1)
        return inches_hg(max(SAFE_MIN, min(SAFE_MAX, pressure)))

    @staticmethod
    def random_temperature(average_temperature: float) -> float:
        # "Safe" constants based roughly on ME.
        # Temperatures are in Celcius.
        SAFE_MIN = -12
        SAFE_MAX = 49
        # Use normalvariate to get normal distribution, more realistic than uniform
        temperature = random.normalvariate(average_temperature, 2)
        temperature = round(temperature)
        return max(SAFE_MIN, min(SAFE_MAX, temperature))

    @staticmethod
    def interpolate_summer_winter(
        summer_value: float, winter_value: float, day: datetime.date
    ) -> float:
        day_of_year = day.timetuple().tm_yday
        day_of_year_peak_summer = 183
        distance_from_peak_summer = abs(-day_of_year_peak_summer + day_of_year)
        winter_factor = distance_from_peak_summer / day_of_year_peak_summer
        return interpolate(summer_value, winter_value, winter_factor, clamp=True)

    @staticmethod
    def interpolate_seasonal_turbulence(
        high_value: float, low_value: float, day: datetime.date
    ) -> float:
        day_of_year = day.timetuple().tm_yday
        day_of_year_peak_summer = 183
        distance_from_peak_summer = -day_of_year_peak_summer + day_of_year

        amplitude = 0.5 * (high_value - low_value)
        offset = amplitude + low_value

        # A high peak in summer and winter, between high_value and low_value.
        return (
            amplitude * math.cos(4 * math.pi * distance_from_peak_summer / 365.25)
            + offset
        )

    @staticmethod
    def interpolate_solar_activity(
        time_of_day: TimeOfDay, high: float, low: float
    ) -> float:
        scale: float = 0

        match time_of_day:
            case TimeOfDay.Dawn:
                scale = 0.4
            case TimeOfDay.Day:
                scale = 1
            case TimeOfDay.Dusk:
                scale = 0.6
            case TimeOfDay.Night:
                scale = 0

        return interpolate(value1=low, value2=high, factor=scale, clamp=True)


class ClearSkies(Weather):
    @property
    def archetype(self) -> WeatherArchetype:
        return WeatherArchetypes.with_id("clear")

    @property
    def pressure_adjustment(self) -> float:
        return 0.22

    @property
    def temperature_adjustment(self) -> float:
        return 3.0

    @property
    def turbulence_adjustment(self) -> float:
        return 0.0

    def generate_clouds(self) -> Optional[Clouds]:
        return None

    def generate_fog(self) -> Optional[Fog]:
        return None


class Cloudy(Weather):
    @property
    def archetype(self) -> WeatherArchetype:
        return WeatherArchetypes.with_id("cloudy")

    @property
    def pressure_adjustment(self) -> float:
        return 0.0

    @property
    def temperature_adjustment(self) -> float:
        return 0.0

    @property
    def turbulence_adjustment(self) -> float:
        return 0.75

    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds.random_preset(rain=False)

    def generate_fog(self) -> Optional[Fog]:
        # DCS 2.7 says to not use fog with the cloud presets.
        return None


class Raining(Weather):
    @property
    def archetype(self) -> WeatherArchetype:
        return WeatherArchetypes.with_id("raining")

    @property
    def pressure_adjustment(self) -> float:
        return -0.22

    @property
    def temperature_adjustment(self) -> float:
        return -3.0

    @property
    def turbulence_adjustment(self) -> float:
        return 1.5

    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds.random_preset(rain=True)

    def generate_fog(self) -> Optional[Fog]:
        # DCS 2.7 says to not use fog with the cloud presets.
        return None


class Thunderstorm(Weather):
    @property
    def archetype(self) -> WeatherArchetype:
        return WeatherArchetypes.with_id("thunderstorm")

    @property
    def pressure_adjustment(self) -> float:
        return 0.1

    @property
    def temperature_adjustment(self) -> float:
        return -3.0

    @property
    def turbulence_adjustment(self) -> float:
        return 3.0

    def generate_clouds(self) -> Optional[Clouds]:
        return Clouds(
            base=self.random_cloud_base(),
            density=random.randint(9, 10),
            thickness=self.random_cloud_thickness(),
            precipitation=PydcsWeather.Preceptions.Thunderstorm,
        )
