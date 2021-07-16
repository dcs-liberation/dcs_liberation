from game.theater.projections import TransverseMercator

PARAMETERS = TransverseMercator(
    central_meridian=39,
    false_easting=282801.00000003993,
    false_northing=-3879865.9999999935,
    scale_factor=0.9996,
)

SEASONAL_CONDITIONS = SeasonalConditions(
    summer_avg_pressure=29.98,  # TODO: More science
    winter_avg_pressure=29.86,  # TODO: More science
    summer_avg_temperature=28.5,
    winter_avg_temperature=10.0,
    temperature_day_night_difference=8.0,

    weather_type_chances={
        # TODO: More science for all these values
        Season.Winter: WeatherTypeChances(
            thunderstorm=1,
            raining=20,
            cloudy=60,
            clear_skies=20,
        ),
        Season.Spring: WeatherTypeChances(
            thunderstorm=1,
            raining=20,
            cloudy=40,
            clear_skies=40,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm=1,
            raining=10,
            cloudy=30,
            clear_skies=60,
        ),
        Season.Autumn: WeatherTypeChances(
            thunderstorm=1,
            raining=30,
            cloudy=50,
            clear_skies=20,
        ),
    },
)
