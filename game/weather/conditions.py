from __future__ import annotations

import datetime
import logging
import random
from dataclasses import dataclass

from game.settings import Settings
from game.theater import ConflictTheater, SeasonalConditions
from game.theater.seasonalconditions import determine_season
from game.timeofday import TimeOfDay, to_datetime
from game.weather.weather import Weather, Thunderstorm, Raining, Cloudy, ClearSkies


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
        return to_datetime(time_of_day, day, theater.terrain, night_disabled)

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
        chances: dict[
            type[ClearSkies] | type[Cloudy] | type[Raining] | type[Thunderstorm], float
        ] = {
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
