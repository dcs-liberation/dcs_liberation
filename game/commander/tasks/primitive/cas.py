from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import FrontLine
from gen.flights.flight import FlightType


@dataclass
class PlanCas(PackagePlanningTask[FrontLine]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.vulnerable_front_lines:
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.vulnerable_front_lines.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.CAS, 2)
        self.propose_flight(FlightType.TARCAP, 2)
