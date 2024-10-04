from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from dcs.weather import Wind

from game.utils import Speed, knots, Heading
from .wind import WindConditions


@dataclass(frozen=True)
class WeibullWindSpeedParameters:
    shape: float
    scale: Speed

    @staticmethod
    def from_data(data: dict[str, Any]) -> WeibullWindSpeedParameters:
        return WeibullWindSpeedParameters(
            shape=data["shape"], scale=knots(data["scale_kts"])
        )


class WindSpeedGenerator(ABC):
    @abstractmethod
    def random_wind(self) -> WindConditions: ...

    @staticmethod
    def from_data(data: dict[str, Any]) -> WindSpeedGenerator:
        if len(data) != 1:
            raise ValueError(
                f"Wind speed dict has wrong number of keys ({len(data)}). Expected 1."
            )
        name = list(data.keys())[0]
        match name:
            case "weibull":
                return WeibullWindSpeedGenerator.from_data(data["weibull"])
        raise KeyError(f"Unknown wind speed generator type: {name}")


class WeibullWindSpeedGenerator(WindSpeedGenerator):
    def __init__(
        self,
        at_msl: WeibullWindSpeedParameters,
        at_2000m: WeibullWindSpeedParameters,
        at_8000m: WeibullWindSpeedParameters,
    ) -> None:
        self.at_msl = at_msl
        self.at_2000m = at_2000m
        self.at_8000m = at_8000m

    def random_wind(self) -> WindConditions:
        wind_direction = Heading.random()
        wind_direction_2000m = wind_direction + Heading.random(-90, 90)
        wind_direction_8000m = wind_direction + Heading.random(-90, 90)

        # The first parameter is the scale. 63.2% of all results will fall below that
        # value.
        # https://www.itl.nist.gov/div898/handbook/eda/section3/weibplot.htm
        msl = random.weibullvariate(
            self.at_msl.scale.meters_per_second, self.at_msl.shape
        )
        at_2000m = random.weibullvariate(
            msl + self.at_2000m.scale.meters_per_second, self.at_2000m.shape
        )
        at_8000m = random.weibullvariate(
            at_2000m + self.at_8000m.scale.meters_per_second, self.at_8000m.shape
        )

        # DCS is limited to 97 knots wind speed.
        max_supported_wind_speed = knots(97).meters_per_second

        return WindConditions(
            # Always some wind to make the smoke move a bit.
            at_0m=Wind(wind_direction.degrees, max(1.0, msl)),
            at_2000m=Wind(
                wind_direction_2000m.degrees,
                min(max_supported_wind_speed, at_2000m),
            ),
            at_8000m=Wind(
                wind_direction_8000m.degrees,
                min(max_supported_wind_speed, at_8000m),
            ),
        )

    @staticmethod
    def from_data(data: dict[str, Any]) -> WindSpeedGenerator:
        return WeibullWindSpeedGenerator(
            at_msl=WeibullWindSpeedParameters.from_data(data["at_msl"]),
            at_2000m=WeibullWindSpeedParameters.from_data(data["at_2000m"]),
            at_8000m=WeibullWindSpeedParameters.from_data(data["at_8000m"]),
        )
