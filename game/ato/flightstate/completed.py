from datetime import datetime, timedelta

from .flightstate import FlightState
from ..starttype import StartType


class Completed(FlightState):
    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
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
