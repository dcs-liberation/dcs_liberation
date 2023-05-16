from __future__ import annotations

from dataclasses import dataclass

from game.utils import Pressure


@dataclass(frozen=True)
class AtmosphericConditions:
    #: Pressure at sea level.
    qnh: Pressure

    #: Temperature at sea level in Celcius.
    temperature_celsius: float

    #: Turbulence per 10 cm.
    turbulence_per_10cm: float
