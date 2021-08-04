from .seasonalconditions import SeasonalConditions, Season, WeatherTypeChances

CONDITIONS = SeasonalConditions(
    summer_avg_pressure=29.98,  # TODO: Find real-world data
    winter_avg_pressure=29.86,  # TODO: Find real-world data
    summer_avg_temperature=28.5,
    winter_avg_temperature=10.0,
    temperature_day_night_difference=8.0,
    weather_type_chances={
        # TODO: Find real-world data for all these values
        Season.Winter: WeatherTypeChances(
            thunderstorm=1,
            raining=25,
            cloudy=35,
            clear_skies=40,
        ),
        Season.Spring: WeatherTypeChances(
            thunderstorm=1,
            raining=10,
            cloudy=30,
            clear_skies=60,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm=1,
            raining=5,
            cloudy=30,
            clear_skies=65,
        ),
        Season.Fall: WeatherTypeChances(
            thunderstorm=1,
            raining=15,
            cloudy=35,
            clear_skies=50,
        ),
    },
)
