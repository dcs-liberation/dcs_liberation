from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .flightstate import FlightState
from .takeoff import Takeoff
from ..starttype import StartType

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.aircraftengagementzones import AircraftEngagementZones


class Taxi(FlightState):
    def __init__(self, flight: Flight, settings: Settings, now: datetime) -> None:
        super().__init__(flight, settings)
        self.completion_time = now + flight.flight_plan.estimate_ground_ops()

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        if time < self.completion_time:
            return
        self.flight.set_state(Takeoff(self.flight, self.settings, time))

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.WARM

    def should_halt_sim(self, enemy_aircraft_coverage: AircraftEngagementZones) -> bool:
        if (
            self.flight.client_count > 0
            and self.settings.player_mission_interrupts_sim_at is StartType.WARM
        ):
            logging.info(
                f"Interrupting simulation because {self.flight} has players and has "
                "reached taxi time"
            )
            return True
        return False
