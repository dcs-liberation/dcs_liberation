from __future__ import annotations

from dataclasses import dataclass

from game.utils import Distance


@dataclass(frozen=True)
class Fog:
    visibility: Distance
    thickness: int
