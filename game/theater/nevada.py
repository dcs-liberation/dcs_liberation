from game.theater.projections import TransverseMercator

PARAMETERS = TransverseMercator(
    central_meridian=-117,
    false_easting=-193996.80999964548,
    false_northing=-4410028.063999966,
    scale_factor=0.9996,
)

SEASONAL_CONDITIONS = SeasonalConditions(
    summer_avg_pressure=30.02,  # TODO: More science
    winter_avg_pressure=29.72,  # TODO: More science
    summer_avg_temperature=31.5,
    winter_avg_temperature=5.0,
    temperature_day_night_difference=6.0,

    weather_type_chances={
        # TODO: More science for all these values
        Season.Winter: WeatherTypeChances(
            thunderstorm=1,
            raining=10,
            cloudy=50,
            clear_skies=40,
        ),
        Season.Spring: WeatherTypeChances(
            thunderstorm=1,
            raining=5,
            cloudy=45,
            clear_skies=50,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm=1,
            raining=5,
            cloudy=25,
            clear_skies=70,
        ),
        Season.Autumn: WeatherTypeChances(
            thunderstorm=1,
            raining=10,
            cloudy=45,
            clear_skies=45,
        ),
    },
)
