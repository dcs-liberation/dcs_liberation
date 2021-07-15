from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.theater import ControlPoint
from gen.flights.flight import FlightType


@dataclass
class PlanBarcap(PackagePlanningTask[ControlPoint]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if not state.barcaps_needed[self.target]:
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.barcaps_needed[self.target] -= 1

    def propose_flights(self, doctrine: Doctrine) -> None:
        self.propose_flight(FlightType.BARCAP, 2, doctrine.mission_ranges.cap)
