from game.theater.projections import TransverseMercator

PARAMETERS = TransverseMercator(
    central_meridian=57,
    false_easting=75755.99999999645,
    false_northing=-2894933.0000000377,
    scale_factor=0.9996,
)

SEASONAL_CONDITIONS = SeasonalConditions(
    summer_avg_pressure=29.98,  # TODO: More science
    winter_avg_pressure=29.80,  # TODO: More science
    summer_avg_temperature=32.5,
    winter_avg_temperature=15.0,
    temperature_day_night_difference=2.0,

    weather_type_chances={
        # TODO: More science for all these values
        Season.Winter: WeatherTypeChances(
            # Winter there is some rain in PG (Dubai)
            thunderstorm=1,
            raining=15,
            cloudy=35,
            clear_skies=50,
        ),
        Season.Spring: WeatherTypeChances(
            thunderstorm=1,
            raining=2,
            cloudy=18,
            clear_skies=80,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm=1,
            raining=1,
            cloudy=8,
            clear_skies=90,
        ),
        Season.Autumn: WeatherTypeChances(
            thunderstorm=1,
            raining=2,
            cloudy=18,
            clear_skies=80,
        ),
    },
)
