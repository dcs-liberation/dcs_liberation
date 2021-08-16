from .seasonalconditions import SeasonalConditions, Season, WeatherTypeChances

CONDITIONS = SeasonalConditions(
    summer_avg_pressure=30.02,  # TODO: Find real-world data
    winter_avg_pressure=29.72,  # TODO: Find real-world data
    summer_avg_temperature=22.5,
    winter_avg_temperature=3.0,
    temperature_day_night_difference=6.0,
    weather_type_chances={
        # TODO: Find real-world data for all these values
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
            cloudy=35,
            clear_skies=55,
        ),
        Season.Fall: WeatherTypeChances(
            thunderstorm=1,
            raining=30,
            cloudy=50,
            clear_skies=20,
        ),
    },
)
