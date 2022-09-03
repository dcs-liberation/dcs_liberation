from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from .flightstate import FlightState
from ..starttype import StartType

if TYPE_CHECKING:
    from game.sim.gameupdateevents import GameUpdateEvents


class Uninitialized(FlightState):
    @property
    def cancelable(self) -> bool:
        return True

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")

    @property
    def is_waiting_for_start(self) -> bool:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")

    def estimate_position(self) -> Point:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")

    @property
    def spawn_type(self) -> StartType:
        raise RuntimeError("Attempted to simulate flight that is not fully initialized")

    @property
    def description(self) -> str:
        delay = self.flight.flight_plan.startup_time()
        if self.flight.start_type is StartType.COLD:
            action = "Starting up"
        elif self.flight.start_type is StartType.WARM:
            action = "Taxiing"
        elif self.flight.start_type is StartType.RUNWAY:
            action = "Taking off"
        elif self.flight.start_type is StartType.IN_FLIGHT:
            action = "In flight"
        else:
            raise ValueError(f"Unhandled StartType: {self.flight.start_type}")
        return f"{action} in {delay}"
