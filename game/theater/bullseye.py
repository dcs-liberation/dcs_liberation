from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, TYPE_CHECKING

from dcs import Point

from game.theater import LatLon

if TYPE_CHECKING:
    from game.theater import ConflictTheater


@dataclass
class Bullseye:
    position: Point

    @classmethod
    def from_pydcs(cls, bulls: Dict[str, float]) -> Bullseye:
        return cls(Point(bulls["x"], bulls["y"]))

    def to_pydcs(self) -> Dict[str, float]:
        return {"x": self.position.x, "y": self.position.y}

    def to_lat_lon(self, theater: ConflictTheater) -> LatLon:
        return theater.point_to_ll(self.position)
