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
