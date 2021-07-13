from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.theater import FrontLine
from gen.flights.flight import FlightType


@dataclass
class PlanCas(PackagePlanningTask[FrontLine]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if not super().preconditions_met(state):
            return False
        return self.target in state.vulnerable_front_lines

    def apply_effects(self, state: TheaterState) -> None:
        state.vulnerable_front_lines.remove(self.target)

    def propose_flights(self, doctrine: Doctrine) -> None:
        self.propose_flight(FlightType.CAS, 2, doctrine.mission_ranges.cas)
        self.propose_flight(FlightType.TARCAP, 2, doctrine.mission_ranges.cap)
