from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .atdeparture import AtDeparture
from .taxi import Taxi
from ..starttype import StartType

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.gameupdateevents import GameUpdateEvents


class StartUp(AtDeparture):
    def __init__(self, flight: Flight, settings: Settings, now: datetime) -> None:
        super().__init__(flight, settings)
        self.completion_time = now + flight.flight_plan.estimate_startup()

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        if time < self.completion_time:
            return
        self.flight.set_state(Taxi(self.flight, self.settings, time))

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.COLD

    def should_halt_sim(self) -> bool:
        if (
            self.flight.client_count > 0
            and self.settings.player_mission_interrupts_sim_at is StartType.COLD
        ):
            logging.info(
                f"Interrupting simulation because {self.flight} has players and has "
                "reached startup time"
            )
            return True
        return False

    @property
    def description(self) -> str:
        return "Starting up"
