from __future__ import annotations

from dataclasses import dataclass
import random

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint
from gen.flights.flight import FlightType


@dataclass
class PlanBarcap(PackagePlanningTask[ControlPoint]):
    max_orders: int

    def preconditions_met(self, state: TheaterState) -> bool:
        if not state.barcaps_needed[self.target]:
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.barcaps_needed[self.target] -= 1

    def propose_flights(self) -> None:
        chances = {
            2: 75,
            3: 5,
            4: 20,
        }
        num_aircraft = random.choices(
            list(chances.keys()), weights=list(chances.values())
        )[0]
        self.propose_flight(FlightType.BARCAP, num_aircraft)

    @property
    def purchase_multiplier(self) -> int:
        return self.max_orders
