from datetime import datetime, timedelta

from .flightstate import FlightState
from ..starttype import StartType


class Uninitialized(FlightState):
    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")

    @property
    def is_waiting_for_start(self) -> bool:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")

    @property
    def spawn_type(self) -> StartType:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")
