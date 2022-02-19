from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from game.ato.starttype import StartType
from .atdeparture import AtDeparture
from .flightstate import FlightState
from .navigating import Navigating
from .startup import StartUp
from .takeoff import Takeoff
from .taxi import Taxi

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.gameupdateevents import GameUpdateEvents


class WaitingForStart(AtDeparture):
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
        return self.flight.start_type

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
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
            new_state = Navigating(self.flight, self.settings, waypoint_index=0)
        self.flight.set_state(new_state)

    @property
    def is_waiting_for_start(self) -> bool:
        return True

    def time_remaining(self, time: datetime) -> timedelta:
        return self.start_time - time

    @property
    def spawn_type(self) -> StartType:
        return self.flight.start_type

    @property
    def description(self) -> str:
        if self.start_type is StartType.COLD:
            start_type = "startup"
        elif self.start_type is StartType.WARM:
            start_type = "taxi"
        elif self.start_type is StartType.RUNWAY:
            start_type = "takeoff"
        elif self.start_type is StartType.IN_FLIGHT:
            start_type = "air start"
        else:
            raise ValueError(f"Unhandled StartType: {self.start_type}")
        return f"Waiting for {start_type} at {self.start_time:%H:%M:%S}"
