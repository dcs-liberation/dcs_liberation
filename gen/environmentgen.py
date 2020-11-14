from typing import Optional

from dcs.mission import Mission

from game.weather import Clouds, Fog, Conditions, WindConditions


class EnvironmentGenerator:
    def __init__(self, mission: Mission, conditions: Conditions) -> None:
        self.mission = mission
        self.conditions = conditions

    def set_clouds(self, clouds: Optional[Clouds]) -> None:
        if clouds is None:
            return
        self.mission.weather.clouds_base = clouds.base
        self.mission.weather.clouds_thickness = clouds.thickness
        self.mission.weather.clouds_density = clouds.density
        self.mission.weather.clouds_iprecptns = clouds.precipitation

    def set_fog(self, fog: Optional[Fog]) -> None:
        if fog is None:
            return
        self.mission.weather.fog_visibility = fog.visibility
        self.mission.weather.fog_thickness = fog.thickness

    def set_wind(self, wind: WindConditions) -> None:
        self.mission.weather.wind_at_ground = wind.at_0m
        self.mission.weather.wind_at_2000 = wind.at_2000m
        self.mission.weather.wind_at_8000 = wind.at_8000m

    def generate(self):
        self.mission.start_time = self.conditions.start_time
        self.set_clouds(self.conditions.weather.clouds)
        self.set_fog(self.conditions.weather.fog)
        self.set_wind(self.conditions.weather.wind)
