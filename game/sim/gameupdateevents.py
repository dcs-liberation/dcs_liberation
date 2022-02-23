from __future__ import annotations

from typing import TYPE_CHECKING

from dcs import Point

if TYPE_CHECKING:
    from game.ato import Flight
    from game.sim.combat import FrozenCombat


class GameUpdateEvents:
    def __init__(self) -> None:
        self.simulation_complete = False
        self.new_combats: list[FrozenCombat] = []
        self.updated_combats: list[FrozenCombat] = []
        self.updated_flights: list[tuple[Flight, Point]] = []
        self.navmesh_updates: set[bool] = set()

    @property
    def empty(self) -> bool:
        return not any(
            [
                self.simulation_complete,
                self.new_combats,
                self.updated_combats,
                self.updated_flights,
                self.navmesh_updates,
            ]
        )

    def complete_simulation(self) -> None:
        self.simulation_complete = True

    def new_combat(self, combat: FrozenCombat) -> None:
        self.new_combats.append(combat)

    def update_combat(self, combat: FrozenCombat) -> None:
        self.updated_combats.append(combat)

    def update_flight(self, flight: Flight, new_position: Point) -> None:
        self.updated_flights.append((flight, new_position))

    def update_navmesh(self, player: bool) -> None:
        self.navmesh_updates.add(player)
