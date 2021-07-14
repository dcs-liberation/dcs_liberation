from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.transfers import CargoShip
from gen.flights.flight import FlightType


@dataclass
class PlanAntiShipping(PackagePlanningTask[CargoShip]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.enemy_shipping:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.enemy_shipping.remove(self.target)

    def propose_flights(self, doctrine: Doctrine) -> None:
        self.propose_flight(FlightType.ANTISHIP, 2, doctrine.mission_ranges.offensive)
        self.propose_common_escorts(doctrine)
