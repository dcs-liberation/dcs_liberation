from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import VehicleGroupGroundObject
from gen.flights.flight import FlightType


@dataclass
class PlanBai(PackagePlanningTask[VehicleGroupGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if not state.has_garrison(self.target):
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.eliminate_garrison(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.BAI, 2)
        self.propose_common_escorts()
