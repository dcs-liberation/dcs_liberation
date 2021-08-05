from .seasonalconditions import SeasonalConditions, Season, WeatherTypeChances

CONDITIONS = SeasonalConditions(
    summer_avg_pressure=30.02,  # TODO: Find real-world data
    winter_avg_pressure=29.72,  # TODO: Find real-world data
    summer_avg_temperature=31.5,
    winter_avg_temperature=5.0,
    temperature_day_night_difference=6.0,
    weather_type_chances={
        # TODO: Find real-world data for all these values
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
            cloudy=30,
            clear_skies=65,
        ),
        Season.Fall: WeatherTypeChances(
            thunderstorm=1,
            raining=10,
            cloudy=45,
            clear_skies=45,
        ),
    },
)
