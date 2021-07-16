import datetime
from dataclasses import dataclass
from enum import Enum

class Season(Enum):
    Winter = "winter"
    Spring = "spring"
    Summer = "summer"
    Autumn = "autumn"

def determine_season(day: datetime.date) -> Season:
    # Note: This logic doesn't need to be very precise
    # TODO: Add support for inverted seasons on southern hemisphere
    day_of_year = day.timetuple().tm_yday
    season_length = 365.0 / 4
    winter_end_day = season_length / 2
    if day_of_year < winter_end_day:
        return Season.Winter
    elif day_of_year < winter_end_day + season_length:
        return Season.Spring
    elif day_of_year < winter_end_day + season_length * 2:
        return Season.Summer
    elif day_of_year < winter_end_day + season_length * 3:
        return Season.Autumn
    else:
        return Season.Winter

@dataclass(frozen=True)
class WeatherTypeChances:
    thunderstorm: float,
    raining: float,
    cloudy: float,
    clear_skies: float,

@dataclass(frozen=True)
class SeasonalConditions:
    # Units are inHg and degrees Celsius
    summer_avg_pressure: float
    winter_avg_pressure: float
    summer_avg_temperature: float
    winter_avg_temperature: float
    temperature_day_night_difference: float

    weather_type_chances: Dict[Season, WeatherTypeChances]
