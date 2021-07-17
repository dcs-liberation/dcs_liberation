from game.theater.projections import TransverseMercator
from .seasonalconditions import SeasonalConditions, Season, WeatherTypeChances

PARAMETERS = TransverseMercator(
    central_meridian=147,
    false_easting=238417.99999989968,
    false_northing=-1491840.000000048,
    scale_factor=0.9996,
)

SEASONAL_CONDITIONS = SeasonalConditions(
    summer_avg_pressure=30.02,  # TODO: Find real-world data
    winter_avg_pressure=29.82,  # TODO: Find real-world data
    summer_avg_temperature=28.0,
    winter_avg_temperature=27.0,
    temperature_day_night_difference=1.0,
    weather_type_chances={
        # TODO: Find real-world data for all these values
        Season.Winter: WeatherTypeChances(
            thunderstorm=2,
            raining=20,
            cloudy=40,
            clear_skies=40,
        ),
        Season.Spring: WeatherTypeChances(
            # Spring is dry/sunny in Marianas
            thunderstorm=1,
            raining=10,
            cloudy=30,
            clear_skies=60,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm=2,
            raining=20,
            cloudy=40,
            clear_skies=40,
        ),
        Season.Fall: WeatherTypeChances(
            # Rain season
            thunderstorm=5,
            raining=45,
            cloudy=30,
            clear_skies=20,
        ),
    },
)
