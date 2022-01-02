from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .flightstate import FlightState
from ..starttype import StartType

if TYPE_CHECKING:
    from game.sim.gameupdateevents import GameUpdateEvents


class Completed(FlightState):
    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        return

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        # TODO: May want to do something different to make these uncontrolled?
        return StartType.COLD

    @property
    def description(self) -> str:
        return "Completed"
