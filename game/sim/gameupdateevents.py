from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.ato import Flight
    from game.sim.combat import FrozenCombat


class GameUpdateEvents:
    def __init__(self) -> None:
        self.simulation_complete = False
        self.new_combats: list[FrozenCombat] = []
        self.updated_combats: list[FrozenCombat] = []
        self.updated_flights: list[Flight] = []

    def complete_simulation(self) -> None:
        self.simulation_complete = True

    def new_combat(self, combat: FrozenCombat) -> None:
        self.new_combats.append(combat)

    def update_combat(self, combat: FrozenCombat) -> None:
        self.updated_combats.append(combat)

    def update_flight(self, flight: Flight) -> None:
        self.updated_flights.append(flight)
