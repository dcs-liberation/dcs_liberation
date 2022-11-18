from datetime import datetime
from typing import Optional

from dcs.mission import Mission

from game.weather import Clouds, Fog, Conditions, WindConditions, AtmosphericConditions


class EnvironmentGenerator:
    def __init__(
        self, mission: Mission, conditions: Conditions, time: datetime
    ) -> None:
        self.mission = mission
        self.conditions = conditions
        self.time = time

    def set_atmospheric(self, atmospheric: AtmosphericConditions) -> None:
        self.mission.weather.qnh = atmospheric.qnh.mm_hg
        self.mission.weather.season_temperature = atmospheric.temperature_celsius
        self.mission.weather.turbulence_at_ground = int(atmospheric.turbulence_per_10cm)

    def set_clouds(self, clouds: Optional[Clouds]) -> None:
        if clouds is None:
            return
        self.mission.weather.clouds_base = clouds.base
        self.mission.weather.clouds_thickness = clouds.thickness
        self.mission.weather.clouds_density = clouds.density
        self.mission.weather.clouds_iprecptns = clouds.precipitation
        self.mission.weather.clouds_preset = clouds.preset

    def set_fog(self, fog: Optional[Fog]) -> None:
        if fog is None:
            return
        self.mission.weather.fog_visibility = int(fog.visibility.meters)
        self.mission.weather.fog_thickness = fog.thickness

    def set_wind(self, wind: WindConditions) -> None:
        self.mission.weather.wind_at_ground = wind.at_0m
        self.mission.weather.wind_at_2000 = wind.at_2000m
        self.mission.weather.wind_at_8000 = wind.at_8000m

    def generate(self) -> None:
        self.mission.start_time = self.time
        self.set_atmospheric(self.conditions.weather.atmospheric)
        self.set_clouds(self.conditions.weather.clouds)
        self.set_fog(self.conditions.weather.fog)
        self.set_wind(self.conditions.weather.wind)
