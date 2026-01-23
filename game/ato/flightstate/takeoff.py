from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from .atdeparture import AtDeparture
from .navigating import Navigating
from ..starttype import StartType
from ...utils import LBS_TO_KG

from game.settings.settings import FastForwardStopCondition

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.gameupdateevents import GameUpdateEvents


class Takeoff(AtDeparture):
    def __init__(self, flight: Flight, settings: Settings, now: datetime) -> None:
        super().__init__(flight, settings)
        # TODO: Not accounted for in FlightPlan, can cause discrepancy without loiter.
        self.completion_time = now + timedelta(seconds=30)

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        if time < self.completion_time:
            return
        self.flight.set_state(Navigating(self.flight, self.settings, waypoint_index=0))

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    @property
    def spawn_type(self) -> StartType:
        return StartType.RUNWAY

    def estimate_fuel(self) -> float:
        initial_fuel = super().estimate_fuel()
        if self.flight.unit_type.fuel_consumption is None:
            return initial_fuel
        return initial_fuel - self.flight.unit_type.fuel_consumption.taxi * LBS_TO_KG

    def should_halt_sim(self) -> bool:
        if (
            self.flight.client_count > 0
            and self.settings.fast_forward_stop_condition
            == FastForwardStopCondition.PLAYER_TAKEOFF
        ):
            logging.info(
                f"Interrupting simulation because {self.flight} has players and has "
                "reached takeoff time"
            )
            return True

        if self.settings.fast_forwward_stop_condition in {
            FastForwardStopCondition.PLAYER_TAXI,
            FastForwardStopCondition.PLAYER_STARTUP,
        }:
            logging.info(
                f"Interrupting simulation because {self.flight} has players and is already taking off "
            )
            return True
        return False

    @property
    def description(self) -> str:
        return "Taking off"
