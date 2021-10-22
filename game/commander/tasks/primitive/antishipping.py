from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.transfers import CargoShip
from game.ato.flighttype import FlightType


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

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.ANTISHIP, 2)
        self.propose_common_escorts()
