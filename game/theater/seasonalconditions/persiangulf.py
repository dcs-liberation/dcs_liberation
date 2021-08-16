from .seasonalconditions import SeasonalConditions, Season, WeatherTypeChances

CONDITIONS = SeasonalConditions(
    summer_avg_pressure=29.98,  # TODO: Find real-world data
    winter_avg_pressure=29.80,  # TODO: Find real-world data
    summer_avg_temperature=32.5,
    winter_avg_temperature=15.0,
    temperature_day_night_difference=2.0,
    weather_type_chances={
        # TODO: Find real-world data for all these values
        Season.Winter: WeatherTypeChances(
            # Winter there is some rain in PG (Dubai)
            thunderstorm=1,
            raining=15,
            cloudy=40,
            clear_skies=45,
        ),
        Season.Spring: WeatherTypeChances(
            thunderstorm=1,
            raining=2,
            cloudy=28,
            clear_skies=70,
        ),
        Season.Summer: WeatherTypeChances(
            thunderstorm=1,
            raining=1,
            cloudy=18,
            clear_skies=80,
        ),
        Season.Fall: WeatherTypeChances(
            thunderstorm=1,
            raining=2,
            cloudy=28,
            clear_skies=70,
        ),
    },
)
