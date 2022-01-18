from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater.theatergroundobject import TheaterGroundObject
from game.ato.flighttype import FlightType


@dataclass
class PlanStrike(PackagePlanningTask[TheaterGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.strike_targets:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.strike_targets.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.STRIKE, 2)
        self.propose_common_escorts()
