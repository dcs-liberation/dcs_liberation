from __future__ import annotations

from dataclasses import dataclass

from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint
from game.ato.flighttype import FlightType


@dataclass
class PlanAirAssault(PackagePlanningTask[ControlPoint]):
    """Task for AirAssault

    TODO: This Task is currently removed from the AutoPlanner
    (removed from Compound Task CaptureBase and removed from TheaterState.
    air_assault_targets) as we can not guarantee that the Flightplan will have
    save landing zones which are free of obstacles (trees, buildings and so on).
    Therefore the AI could potentially crash when Missions are autoplanned and not
    validated manually from the user
    """

    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.air_assault_targets:
            return False
        # TODO add check if there is a safe Landingzone available next to the CP which
        # we can use to AutoPlan the Mission. Possible implementation for this
        # functionality could be to let the campaign designer define possible zones
        # which the planner can use.
        if self.capture_blocked(state):
            # Do not task if there are enemy battle_positions blocking the capture
            return False
        if not self.target_area_preconditions_met(state):
            # Do not task if air defense is present in the target area
            return False
        return super().preconditions_met(state)

    def capture_blocked(self, state: TheaterState) -> bool:
        battle_positions = state.enemy_battle_positions[self.target]
        return len(battle_positions.blocking_capture) > 0

    def apply_effects(self, state: TheaterState) -> None:
        state.air_assault_targets.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.AIR_ASSAULT, 2)
        # TODO Validate this.. / is Heli escort possible?
        self.propose_flight(FlightType.TARCAP, 2)
