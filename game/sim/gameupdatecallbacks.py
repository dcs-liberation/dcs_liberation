from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from game.sim.gameupdateevents import GameUpdateEvents


# Ought to be frozen but mypy can't handle that:
# https://github.com/python/mypy/issues/5485
@dataclass
class GameUpdateCallbacks:
    on_simulation_complete: Callable[[], None]
    on_update: Callable[[GameUpdateEvents], None]
