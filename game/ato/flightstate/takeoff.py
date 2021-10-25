from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .flightstate import FlightState
from .inflight import InFlight
from ..starttype import StartType

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings


class Takeoff(FlightState):
    def __init__(self, flight: Flight, settings: Settings, now: datetime) -> None:
        super().__init__(flight, settings)
        # TODO: Not accounted for in FlightPlan, can cause discrepancy without loiter.
        self.completion_time = now + timedelta(seconds=30)

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        if time < self.completion_time:
            return
        self.flight.set_state(InFlight(self.flight, self.settings))

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.RUNWAY

    def should_halt_sim(self) -> bool:
        if (
            self.flight.client_count > 0
            and self.settings.player_mission_interrupts_sim_at is StartType.RUNWAY
        ):
            logging.info(
                f"Interrupting simulation because {self.flight} has players and has "
                "reached takeoff time"
            )
            return True
        return False
