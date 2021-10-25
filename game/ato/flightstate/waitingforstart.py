from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from game.ato.starttype import StartType
from .flightstate import FlightState
from .inflight import InFlight
from .startup import StartUp
from .takeoff import Takeoff
from .taxi import Taxi

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings


class WaitingForStart(FlightState):
    def __init__(
        self,
        flight: Flight,
        settings: Settings,
        start_time: datetime,
    ) -> None:
        super().__init__(flight, settings)
        self.start_time = start_time

    @property
    def start_type(self) -> StartType:
        return self.flight.get_start_type

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        if time < self.start_time:
            return

        new_state: FlightState
        if self.start_type is StartType.COLD:
            new_state = StartUp(self.flight, self.settings, time)
        elif self.start_type is StartType.WARM:
            new_state = Taxi(self.flight, self.settings, time)
        elif self.start_type is StartType.RUNWAY:
            new_state = Takeoff(self.flight, self.settings, time)
        else:
            new_state = InFlight(self.flight, self.settings)
        self.flight.set_state(new_state)

    @property
    def is_waiting_for_start(self) -> bool:
        return True

    def time_remaining(self, time: datetime) -> timedelta:
        return self.start_time - time

    @property
    def spawn_type(self) -> StartType:
        return self.flight.get_start_type
