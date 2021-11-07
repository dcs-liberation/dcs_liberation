from __future__ import annotations

import itertools
from collections.abc import Iterator
from datetime import datetime, timedelta

from typing_extensions import TYPE_CHECKING

from game.ato import Flight
from game.ato.flightstate import (
    Navigating,
    StartUp,
    Takeoff,
    Taxi,
    Uninitialized,
    WaitingForStart,
)
from game.ato.starttype import StartType
from gen.flights.traveltime import TotEstimator
from .combat import CombatInitiator, FrozenCombat

if TYPE_CHECKING:
    from game import Game


class AircraftSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.combats: list[FrozenCombat] = []

    def begin_simulation(self) -> None:
        self.reset()
        self.set_initial_flight_states()

    def on_game_tick(self, time: datetime, duration: timedelta) -> bool:
        for flight in self.iter_flights():
            flight.on_game_tick(time, duration)

        # Finish updating all flights before checking for combat so that the new
        # positions are used.
        CombatInitiator(self.game, self.combats).update_active_combats()

        # After updating all combat states, check for halts.
        for flight in self.iter_flights():
            if flight.should_halt_sim():
                return True
        return False

    def set_initial_flight_states(self) -> None:
        now = self.game.conditions.start_time
        for flight in self.iter_flights():
            estimator = TotEstimator(flight.package)
            start_time = estimator.mission_start_time(flight)
            if start_time <= timedelta():
                self.set_active_flight_state(flight, now)
            else:
                flight.set_state(
                    WaitingForStart(flight, self.game.settings, now + start_time)
                )

    def set_active_flight_state(self, flight: Flight, now: datetime) -> None:
        if flight.start_type is StartType.COLD:
            flight.set_state(StartUp(flight, self.game.settings, now))
        elif flight.start_type is StartType.WARM:
            flight.set_state(Taxi(flight, self.game.settings, now))
        elif flight.start_type is StartType.RUNWAY:
            flight.set_state(Takeoff(flight, self.game.settings, now))
        elif flight.start_type is StartType.IN_FLIGHT:
            flight.set_state(Navigating(flight, self.game.settings, waypoint_index=0))
        else:
            raise ValueError(f"Unknown start type {flight.start_type} for {flight}")

    def reset(self) -> None:
        for flight in self.iter_flights():
            flight.set_state(Uninitialized(flight, self.game.settings))

    def iter_flights(self) -> Iterator[Flight]:
        packages = itertools.chain(
            self.game.blue.ato.packages, self.game.red.ato.packages
        )
        for package in packages:
            yield from package.flights
