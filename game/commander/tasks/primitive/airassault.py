from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint
from game.ato.flighttype import FlightType


@dataclass
class PlanAirAssault(PackagePlanningTask[ControlPoint]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.air_assault_targets:
            return False
        if self.capture_blocked(state):
            # Do not task if there are enemy garrisons blocking the capture
            return False
        if not self.target_area_preconditions_met(state):
            # Do not task if air defense is present in the target area
            return False
        return super().preconditions_met(state)

    def capture_blocked(self, state: TheaterState) -> bool:
        garrisons = state.enemy_garrisons[self.target]
        return len(garrisons.blocking_capture) > 0

    def apply_effects(self, state: TheaterState) -> None:
        state.air_assault_targets.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.AIR_ASSAULT, 2)
        # TODO Validate this.. / is Heli escort possible?
        self.propose_flight(FlightType.TARCAP, 2)
