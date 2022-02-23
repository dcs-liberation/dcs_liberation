from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from dcs import Point


@dataclass
class Bullseye:
    position: Point

    def to_pydcs(self) -> Dict[str, float]:
        return {"x": self.position.x, "y": self.position.y}
