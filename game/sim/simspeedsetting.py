from __future__ import annotations

from enum import Enum, unique


@unique
class SimSpeedSetting(Enum):
    PAUSED = (0, "Paused")
    X1 = (1, "1x")
    X2 = (2, "2x")
    X5 = (5, "5x")
    X10 = (10, "10x")
    X100 = (100, "100x")
    X1000 = (1000, "1000x")

    def __init__(self, speed_factor: int, text: str) -> None:
        self.speed_factor = speed_factor
        self.text = text

    def __str__(self) -> str:
        return self.text

    @classmethod
    def from_factor(cls, speed_factor: int) -> SimSpeedSetting:
        for setting in SimSpeedSetting:
            if setting.speed_factor == speed_factor:
                return setting
        raise ValueError
