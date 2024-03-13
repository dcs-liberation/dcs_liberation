from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.settings import Settings
from .flightstate import FlightState
from ..starttype import StartType

if TYPE_CHECKING:
    from .. import Flight
    from game.sim.gameupdateevents import GameUpdateEvents


class Killed(FlightState):
    def __init__(
        self, last_position: Point, flight: Flight, settings: Settings
    ) -> None:
        super().__init__(flight, settings)
        self.last_position = last_position

    @property
    def cancelable(self) -> bool:
        return False

    @property
    def alive(self) -> bool:
        return False

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        return

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    def estimate_position(self) -> Point:
        return self.last_position

    @property
    def spawn_type(self) -> StartType:
        raise RuntimeError("Attempted to spawn a dead flight")

    @property
    def description(self) -> str:
        return "KIA"
