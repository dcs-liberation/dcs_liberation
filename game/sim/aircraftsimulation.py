from __future__ import annotations

import itertools
import logging
from collections.abc import Iterator
from datetime import datetime, timedelta

from typing_extensions import TYPE_CHECKING

from game.ato.flightstate import (
    Uninitialized,
)
from .combat import CombatInitiator, FrozenCombat
from .simulationresults import SimulationResults

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight
    from .gameupdateevents import GameUpdateEvents


class AircraftSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.combats: list[FrozenCombat] = []
        self.results = SimulationResults()

    def begin_simulation(self) -> None:
        self.reset()
        self.set_initial_flight_states()

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        if not self.game.settings.auto_resolve_combat and self.combats:
            logging.error(
                "Cannot resume simulation because aircraft are in combat and "
                "auto-resolve is disabled"
            )
            events.complete_simulation()
            return

        still_active = []
        for combat in self.combats:
            if combat.on_game_tick(time, duration, self.results, events):
                events.end_combat(combat)
            else:
                still_active.append(combat)
        self.combats = still_active

        for flight in self.iter_flights():
            flight.on_game_tick(events, time, duration)

        # Finish updating all flights before checking for combat so that the new
        # positions are used.
        CombatInitiator(self.game, self.combats, events).update_active_combats()

        # After updating all combat states, check for halts.
        for flight in self.iter_flights():
            if flight.should_halt_sim():
                events.complete_simulation()
                return

        if not self.game.settings.auto_resolve_combat and self.combats:
            events.complete_simulation()

    def set_initial_flight_states(self) -> None:
        now = self.game.conditions.start_time
        for flight in self.iter_flights():
            flight.state.reinitialize(now)

    def reset(self) -> None:
        for flight in self.iter_flights():
            flight.set_state(Uninitialized(flight, self.game.settings))

    def iter_flights(self) -> Iterator[Flight]:
        packages = itertools.chain(
            self.game.blue.ato.packages, self.game.red.ato.packages
        )
        for package in packages:
            yield from package.flights
