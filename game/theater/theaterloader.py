from __future__ import annotations

import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dcs.terrain import (
    Caucasus,
    Falklands,
    MarianaIslands,
    Nevada,
    Normandy,
    PersianGulf,
    Syria,
    TheChannel,
)

from .conflicttheater import ConflictTheater
from .daytimemap import DaytimeMap
from .landmap import load_landmap
from .seasonalconditions import Season, SeasonalConditions, WeatherTypeChances

ALL_TERRAINS = [
    Caucasus(),
    Falklands(),
    PersianGulf(),
    Normandy(),
    MarianaIslands(),
    Nevada(),
    TheChannel(),
    Syria(),
]

TERRAINS_BY_NAME = {t.name: t for t in ALL_TERRAINS}


@dataclass(frozen=True)
class SeasonData:
    average_temperature: float | None
    average_pressure: float | None
    weather: WeatherTypeChances

    @staticmethod
    def from_yaml(data: dict[str, Any]) -> SeasonData:
        return SeasonData(
            data.get("average_temperature"),
            data.get("average_pressure"),
            WeatherTypeChances(
                data["weather"]["thunderstorm"],
                data["weather"]["raining"],
                data["weather"]["cloudy"],
                data["weather"]["clear"],
            ),
        )


class TheaterLoader:
    def __init__(self, name: str) -> None:
        self.name = name
        self.descriptor_path = Path("resources/theaters") / self.name / "info.yaml"

    def load(self) -> ConflictTheater:
        with self.descriptor_path.open() as descriptor_file:
            data = yaml.safe_load(descriptor_file)
        return ConflictTheater(
            TERRAINS_BY_NAME[data.get("pydcs_name", data["name"])],
            load_landmap(self.descriptor_path.with_name("landmap.p")),
            datetime.timezone(datetime.timedelta(hours=data["timezone"])),
            self._load_seasonal_conditions(data["climate"]),
            self._load_daytime_map(data["daytime"]),
        )

    def _load_daytime_map(self, daytime_data: dict[str, list[int]]) -> DaytimeMap:
        return DaytimeMap(
            dawn=self._load_daytime_range(daytime_data["dawn"]),
            day=self._load_daytime_range(daytime_data["day"]),
            dusk=self._load_daytime_range(daytime_data["dusk"]),
            night=self._load_daytime_range(daytime_data["night"]),
        )

    @staticmethod
    def _load_daytime_range(
        daytime_range: list[int],
    ) -> tuple[datetime.time, datetime.time]:
        begin, end = daytime_range
        return datetime.time(hour=begin), datetime.time(hour=end)

    def _load_seasonal_conditions(
        self, climate_data: dict[str, Any]
    ) -> SeasonalConditions:
        winter = SeasonData.from_yaml(climate_data["seasons"]["winter"])
        spring = SeasonData.from_yaml(climate_data["seasons"]["spring"])
        summer = SeasonData.from_yaml(climate_data["seasons"]["summer"])
        fall = SeasonData.from_yaml(climate_data["seasons"]["fall"])
        if summer.average_pressure is None:
            raise RuntimeError(
                f"{self.descriptor_path} does not define a summer average pressure"
            )
        if summer.average_temperature is None:
            raise RuntimeError(
                f"{self.descriptor_path} does not define a summer average temperature"
            )
        if winter.average_pressure is None:
            raise RuntimeError(
                f"{self.descriptor_path} does not define a winter average pressure"
            )
        if winter.average_temperature is None:
            raise RuntimeError(
                f"{self.descriptor_path} does not define a winter average temperature"
            )
        return SeasonalConditions(
            summer.average_pressure,
            winter.average_pressure,
            summer.average_temperature,
            winter.average_temperature,
            climate_data["day_night_temperature_difference"],
            {
                Season.Winter: winter.weather,
                Season.Spring: spring.weather,
                Season.Summer: summer.weather,
                Season.Fall: fall.weather,
            },
        )
