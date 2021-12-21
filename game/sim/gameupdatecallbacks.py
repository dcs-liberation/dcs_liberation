from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.sim.combat import FrozenCombat


# Ought to be frozen but mypy can't handle that:
# https://github.com/python/mypy/issues/5485
@dataclass
class GameUpdateCallbacks:
    on_simulation_complete: Callable[[], None]
    on_add_combat: Callable[[FrozenCombat], None]
    on_combat_changed: Callable[[FrozenCombat], None]
