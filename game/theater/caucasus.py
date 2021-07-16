from game.theater.projections import TransverseMercator
from game.seasonalconditions import SeasonalConditions, Season, WeatherTypeChances

PARAMETERS = TransverseMercator(
    central_meridian=33,
    false_easting=-99516.9999999732,
    false_northing=-4998114.999999984,
    scale_factor=0.9996,
)

SEASONAL_CONDITIONS = SeasonalConditions:
    summer_avg_pressure=30.02,  # TODO: More science
    winter_avg_pressure=29.72,  # TODO: More science
    summer_avg_temperature=22.5,
    winter_avg_temperature=3.0,
    temperature_day_night_difference=6.0,

    weather_type_chances: {
        # TODO: More science for all these values
        Season.Winter: WeatherTypeChances(
            thunderstorm: 1,
            raining: 20,
            cloudy: 60,
            clear_skies: 20,
        ),
        Season.Spring: WeatherTypeChances(
            thunderstorm: 1,
            raining: 20,
            cloudy: 40,
            clear_skies: 40,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm: 1,
            raining: 10,
            cloudy: 30,
            clear_skies: 60,
        ),
        Season.Autumn: WeatherTypeChances(
            thunderstorm: 1,
            raining: 30,
            cloudy: 50,
            clear_skies: 20,
        )
    }
)
