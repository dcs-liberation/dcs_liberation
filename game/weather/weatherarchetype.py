from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .windspeedgenerators import WindSpeedGenerator


@dataclass(frozen=True)
class WindParameters:
    speed: WindSpeedGenerator

    @staticmethod
    def from_data(data: dict[str, Any]) -> WindParameters:
        return WindParameters(speed=WindSpeedGenerator.from_data(data["speed"]))


@dataclass(frozen=True)
class WeatherArchetype:
    id: str
    wind_parameters: WindParameters

    @staticmethod
    def from_data(data: dict[str, Any]) -> WeatherArchetype:
        return WeatherArchetype(
            id=data["id"], wind_parameters=WindParameters.from_data(data["wind"])
        )

    @staticmethod
    def from_yaml(path: Path) -> WeatherArchetype:
        with path.open(encoding="utf-8") as yaml_file:
            data = yaml.safe_load(yaml_file)
        return WeatherArchetype.from_data(data)


class WeatherArchetypes:
    _by_id: dict[str, WeatherArchetype] | None = None

    @classmethod
    def with_id(cls, ident: str) -> WeatherArchetype:
        if cls._by_id is None:
            cls._by_id = cls.load()
        return cls._by_id[ident]

    @staticmethod
    def load() -> dict[str, WeatherArchetype]:
        by_id = {}
        for path in Path("resources/weather/archetypes").glob("*.yaml"):
            archetype = WeatherArchetype.from_yaml(path)
            if archetype.id in by_id:
                raise RuntimeError(
                    f"Found duplicate weather archetype ID: {archetype.id}"
                )
            by_id[archetype.id] = archetype
        return by_id
