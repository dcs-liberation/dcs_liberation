from game.theater.projections import TransverseMercator

PARAMETERS = TransverseMercator(
    central_meridian=147,
    false_easting=238417.99999989968,
    false_northing=-1491840.000000048,
    scale_factor=0.9996,
)

SEASONAL_CONDITIONS = SeasonalConditions(
    summer_avg_pressure=30.02,  # TODO: More science
    winter_avg_pressure=29.82,  # TODO: More science
    summer_avg_temperature=28.0,
    winter_avg_temperature=27.0,
    temperature_day_night_difference=1.0,

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
