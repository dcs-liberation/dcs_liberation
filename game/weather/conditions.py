from __future__ import annotations

import datetime
import logging
import random
from dataclasses import dataclass

from game.settings import Settings
from game.theater import ConflictTheater, DaytimeMap, SeasonalConditions
from game.theater.seasonalconditions import determine_season
from game.timeofday import TimeOfDay
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
