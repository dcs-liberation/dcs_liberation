import abc
from dataclasses import dataclass

from dcs import Point

from game.utils import Distance


@dataclass(frozen=True)
class UiZone:
    points: list[Point]
    radius: Distance


class UiZoneDisplay(abc.ABC):
    @abc.abstractmethod
    def ui_zone(self) -> UiZone:
        ...
