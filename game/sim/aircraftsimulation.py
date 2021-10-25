from __future__ import annotations

import itertools
import logging
from collections import Iterator
from datetime import datetime, timedelta

from typing_extensions import TYPE_CHECKING

from game.ato import Flight
from game.ato.flightstate import (
    InFlight,
    StartUp,
    Takeoff,
    Taxi,
    Uninitialized,
    WaitingForStart,
)
from game.ato.starttype import StartType
from gen.flights.traveltime import TotEstimator

if TYPE_CHECKING:
    from game import Game


TICK = timedelta(seconds=1)


class AircraftSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.time = self.game.conditions.start_time

    def run(self) -> None:
        self.reset()
        self.set_initial_flight_states()
        if self.game.settings.fast_forward_to_first_contact:
            self.simulate_until_first_contact()
            logging.info(f"Mission simulation completed at {self.time}")

    def simulate_until_first_contact(self) -> None:
        while True:
            self.time += TICK
            if self.tick():
                return

    def tick(self) -> bool:
        interrupt_sim = False
        for flight in self.iter_flights():
            if flight.on_game_tick(self.time, TICK):
                interrupt_sim = True

        # TODO: Check for SAM or A2A contact.
        # Generate an engagement poly for all active air-to-air aircraft per-coalition
        # and compare those against aircraft positions. If any aircraft intersects an
        # enemy air-threat region, generate the mission. Also check against enemy SAM
        # zones.
        return interrupt_sim

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
        if flight.get_start_type is StartType.COLD:
            flight.set_state(StartUp(flight, self.game.settings, now))
        elif flight.get_start_type is StartType.WARM:
            flight.set_state(Taxi(flight, self.game.settings, now))
        elif flight.get_start_type is StartType.RUNWAY:
            flight.set_state(Takeoff(flight, self.game.settings, now))
        elif flight.get_start_type is StartType.IN_FLIGHT:
            flight.set_state(InFlight(flight, self.game.settings))
        else:
            raise ValueError(f"Unknown start type {flight.get_start_type} for {flight}")

    def reset(self) -> None:
        self.time = self.game.conditions.start_time
        for flight in self.iter_flights():
            flight.set_state(Uninitialized(flight, self.game.settings))

    def iter_flights(self) -> Iterator[Flight]:
        packages = itertools.chain(
            self.game.blue.ato.packages, self.game.red.ato.packages
        )
        for package in packages:
            yield from package.flights
