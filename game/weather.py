from __future__ import annotations

import datetime
import logging
import math
import random
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from dcs.cloud_presets import Clouds as PydcsClouds
from dcs.weather import CloudPreset, Weather as PydcsWeather, Wind

from game.theater.daytimemap import DaytimeMap
from game.theater.seasonalconditions import determine_season
from game.timeofday import TimeOfDay
from game.utils import (
    Distance,
    Heading,
    Pressure,
    inches_hg,
    interpolate,
    knots,
    meters,
)

if TYPE_CHECKING:
    from game.settings import Settings
    from game.theater import ConflictTheater
    from game.theater.seasonalconditions import SeasonalConditions


@dataclass(frozen=True)
class AtmosphericConditions:
    #: Pressure at sea level.
    qnh: Pressure

    #: Temperature at sea level in Celcius.
    temperature_celsius: float

    #: Turbulence per 10 cm.
    turbulence_per_10cm: float


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
        raise NotImplementedError

    @staticmethod
    def random_wind(minimum: int, maximum: int) -> WindConditions:
        wind_direction = Heading.random()
        wind_direction_2000m = wind_direction + Heading.random(-90, 90)
        wind_direction_8000m = wind_direction + Heading.random(-90, 90)
        at_0m_factor = 1
        at_2000m_factor = 3 + random.choice([0, 0, 0, 0, 0, 1, 1])

        high_alt_variation = random.choice(
            [
                -3,
                -3,
                -2,
                -2,
                -2,
                -2,
                -2,
                -2,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                0,
                0,
                0,
                1,
                1,
                2,
                3,
            ]
        )
        at_8000m_factor = at_2000m_factor + 5 + high_alt_variation

        base_wind = random.randint(minimum, maximum)

        # DCS is limited to 97 knots wind speed.
        max_supported_wind_speed = knots(97).meters_per_second

        return WindConditions(
            # Always some wind to make the smoke move a bit.
            at_0m=Wind(wind_direction.degrees, max(1, base_wind * at_0m_factor)),
            at_2000m=Wind(
                wind_direction_2000m.degrees,
                min(max_supported_wind_speed, base_wind * at_2000m_factor),
            ),
            at_8000m=Wind(
                wind_direction_8000m.degrees,
                min(max_supported_wind_speed, base_wind * at_8000m_factor),
            ),
        )

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

    def generate_wind(self) -> WindConditions:
        return self.random_wind(1, 4)


class Cloudy(Weather):
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

    def generate_wind(self) -> WindConditions:
        return self.random_wind(2, 4)


class Raining(Weather):
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

    def generate_wind(self) -> WindConditions:
        return self.random_wind(2, 6)


class Thunderstorm(Weather):
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

    def generate_wind(self) -> WindConditions:
        return self.random_wind(2, 8)


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
        forced_time: datetime.time | None = None,
    ) -> Conditions:
        # The time might be forced by the campaign for the first turn.
        if forced_time is not None:
            _start_time = datetime.datetime.combine(day, forced_time)
        else:
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
            time_range = DaytimeMap(
                dawn=(datetime.time(hour=8), datetime.time(hour=9)),
                day=(datetime.time(hour=10), datetime.time(hour=12)),
                dusk=(datetime.time(hour=12), datetime.time(hour=14)),
                night=(datetime.time(hour=14), datetime.time(hour=17)),
            ).range_of(time_of_day)
        else:
            time_range = theater.daytime_map.range_of(time_of_day)

        # Starting missions on the hour is a nice gameplay property, so keep the random
        # time constrained to that. DaytimeMap enforces that we have only whole hour
        # ranges for now, so we don't need to worry about accidentally changing the time
        # of day by truncating sub-hours.
        time = datetime.time(
            hour=random.randint(time_range[0].hour, time_range[1].hour)
        )
        return datetime.datetime.combine(day, time)

    @classmethod
    def generate_weather(
        cls,
        seasonal_conditions: SeasonalConditions,
        day: datetime.date,
        time_of_day: TimeOfDay,
    ) -> Weather:
        season = determine_season(day)
        logging.debug("Weather: Season {}".format(season))
        weather_chances = seasonal_conditions.weather_type_chances[season]
        chances = {
            Thunderstorm: weather_chances.thunderstorm,
            Raining: weather_chances.raining,
            Cloudy: weather_chances.cloudy,
            ClearSkies: weather_chances.clear_skies,
        }
        logging.debug("Weather: Chances {}".format(weather_chances))
        weather_type = random.choices(
            list(chances.keys()), weights=list(chances.values())
        )[0]
        logging.debug("Weather: Type {}".format(weather_type))
        return weather_type(seasonal_conditions, day, time_of_day)
