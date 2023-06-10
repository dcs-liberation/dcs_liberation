from __future__ import annotations

from dataclasses import dataclass

from dcs.weather import Wind


@dataclass(frozen=True)
class WindConditions:
    at_0m: Wind
    at_2000m: Wind
    at_8000m: Wind
