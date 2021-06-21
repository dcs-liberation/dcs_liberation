from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.transfers import Convoy
from gen.flights.flight import FlightType


@dataclass
class PlanConvoyInterdiction(PackagePlanningTask[Convoy]):
    def preconditions_met(self, state: TheaterState) -> bool:
        return self.target in state.enemy_convoys

    def apply_effects(self, state: TheaterState) -> None:
        state.enemy_convoys.remove(self.target)

    def propose_flights(self, doctrine: Doctrine) -> None:
        self.propose_flight(FlightType.BAI, 2, doctrine.mission_ranges.offensive)
        self.propose_common_escorts(doctrine)
