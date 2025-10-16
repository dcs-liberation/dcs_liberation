from __future__ import annotations

import itertools
import logging
from collections.abc import Iterator
from datetime import datetime, timedelta

from typing_extensions import TYPE_CHECKING

from game.ato.flightstate import Uninitialized, Completed, InCombat
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
        self,
        events: GameUpdateEvents,
        time: datetime,
        duration: timedelta,
        combat_resolution_method: CombatResolutionMethod,
        force_continue: bool,
    ) -> None:
        if (
            not self._auto_resolve_combat(combat_resolution_method, force_continue)
            and self.combats
        ):
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
                combat_resolution_method,
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
            if flight.should_halt_sim() and not force_continue:
                events.complete_simulation()
                return

        # Find completed flights, removing them from the ATO and returning aircraft
        # and pilots back to the squadron.
        for flight in self.iter_flights():
            if type(flight.state) == Completed:
                flight.package.remove_flight(flight)
                if len(flight.package.flights) == 0:
                    flight.squadron.coalition.ato.remove_package(flight.package)

        if (
            not self._auto_resolve_combat(combat_resolution_method, force_continue)
            and self.combats
        ):
            events.complete_simulation()

    def set_initial_flight_states(self) -> None:
        # Initialize flights in Uninitialized state
        now = self.game.simulation_time
        for flight in self.iter_flights():
            flight.state.initialize(now)

        # Recover combat instances from flight states. Flight state information is serialized
        # when saving a game but the aircraft simulation state is not. Combat instances are
        # de-duplicated as multiple flights can be involved in a single combat instance.
        combats = set()
        for flight in self.iter_flights():
            if type(flight.state) == InCombat:
                combats.add(flight.state.combat)
        self.combats = list(combats)

    def iter_flights(self) -> Iterator[Flight]:
        packages = itertools.chain(
            self.game.blue.ato.packages, self.game.red.ato.packages
        )
        for package in packages:
            yield from package.flights

    def _auto_resolve_combat(
        self, combat_resolution_method: CombatResolutionMethod, force_continue: bool
    ) -> bool:
        if force_continue:
            return True
        return combat_resolution_method != CombatResolutionMethod.PAUSE
