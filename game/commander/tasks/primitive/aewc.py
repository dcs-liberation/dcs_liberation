from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import MissionTarget
from game.ato.flighttype import FlightType


@dataclass
class PlanAewc(PackagePlanningTask[MissionTarget]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if not super().preconditions_met(state):
            return False
        return self.target in state.aewc_targets

    def apply_effects(self, state: TheaterState) -> None:
        state.aewc_targets.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.AEWC, 1)

    @property
    def asap(self) -> bool:
        # Supports all the early CAP flights, so should be in the air ASAP.
        return True
