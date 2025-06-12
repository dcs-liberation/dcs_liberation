from __future__ import annotations

import itertools
import logging
from collections.abc import Iterator
from datetime import datetime, timedelta

from typing_extensions import TYPE_CHECKING

from game.ato.flightstate import Uninitialized, Completed
from game.settings.settings import FastForwardStopCondition, CombatResolutionMethod
from .combat import CombatInitiator, FrozenCombat
from .gameupdateevents import GameUpdateEvents
from .simulationresults import SimulationResults

if TYPE_CHECKING:
    from game import Game
    from game.ato import Flight


class AircraftSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.combats: list[FrozenCombat] = []
        self.results = SimulationResults()

    def begin_simulation(self) -> None:
        self.set_initial_flight_states()

    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        if not self._auto_resolve_combat() and self.combats:
            logging.error(
                "Cannot resume simulation because aircraft are in combat and "
                "auto-resolve is disabled"
            )
            events.complete_simulation()
            return

        still_active = []
        for combat in self.combats:
            if combat.on_game_tick(
                time,
                duration,
                self.results,
                events,
                self.game.settings.combat_resolution_method,
            ):
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

        # Find completed flights, removing them from the ATO and returning aircraft
        # and pilots back to the squadron.
        for flight in self.iter_flights():
            if type(flight.state) == Completed:
                flight.return_pilots_and_aircraft()
                flight.package.remove_flight(flight)
                if len(flight.package.flights) == 0:
                    flight.squadron.coalition.ato.remove_package(flight.package)

        if not self._auto_resolve_combat() and self.combats:
            events.complete_simulation()

    def set_initial_flight_states(self) -> None:
        now = self.game.simulation_time
        for flight in self.iter_flights():
            flight.state.initialize(now)

    def iter_flights(self) -> Iterator[Flight]:
        packages = itertools.chain(
            self.game.blue.ato.packages, self.game.red.ato.packages
        )
        for package in packages:
            yield from package.flights

    def _auto_resolve_combat(self) -> bool:
        return (
            self.game.settings.fast_forward_stop_condition
            != FastForwardStopCondition.DISABLED
            and self.game.settings.combat_resolution_method
            != CombatResolutionMethod.PAUSE
        )
