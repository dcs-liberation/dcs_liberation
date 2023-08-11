from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.flightplan.waypointactions.waypointaction import WaypointAction


class ActionState:
    def __init__(self, action: WaypointAction) -> None:
        self.action = action
        self._finished = False

    def describe(self) -> str:
        return self.action.describe()

    def finish(self) -> None:
        self._finished = True

    def is_finished(self) -> bool:
        return self._finished

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        self.action.update_state(self, time, duration)
