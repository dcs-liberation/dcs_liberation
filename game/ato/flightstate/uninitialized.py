from datetime import datetime, timedelta

from gen.flights.traveltime import TotEstimator
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

    @property
    def description(self) -> str:
        estimator = TotEstimator(self.flight.package)
        delay = estimator.mission_start_time(self.flight)
        return f"Starting in {delay}"
