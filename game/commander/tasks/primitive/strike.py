from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.theater.theatergroundobject import TheaterGroundObject
from gen.flights.flight import FlightType


@dataclass
class PlanStrike(PackagePlanningTask[TheaterGroundObject[Any]]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.strike_targets:
            return False
        return self.target_area_preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.strike_targets.remove(self.target)

    def propose_flights(self, doctrine: Doctrine) -> None:
        self.propose_flight(FlightType.STRIKE, 2, doctrine.mission_ranges.offensive)
        self.propose_common_escorts(doctrine)
