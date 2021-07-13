from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from game.commander.missionproposals import ProposedMission, ProposedFlight
from game.commander.tasks.theatercommandertask import TheaterCommanderTask
from game.commander.theaterstate import TheaterState
from game.profiling import MultiEventTracer
from game.theater import ControlPoint
from gen.flights.flight import FlightType

if TYPE_CHECKING:
    from gen.flights.ai_flight_planner import CoalitionMissionPlanner


@dataclass
class PlanBarcap(TheaterCommanderTask):
    target: ControlPoint
    rounds: int

    def preconditions_met(self, state: TheaterState) -> bool:
        if state.player and not state.ato_automation_enabled:
            return False
        return self.target in state.vulnerable_control_points

    def apply_effects(self, state: TheaterState) -> None:
        state.vulnerable_control_points.remove(self.target)

    def execute(
        self, mission_planner: CoalitionMissionPlanner, tracer: MultiEventTracer
    ) -> None:
        for _ in range(self.rounds):
            mission_planner.plan_mission(
                ProposedMission(
                    self.target,
                    [
                        ProposedFlight(
                            FlightType.BARCAP,
                            2,
                            mission_planner.doctrine.mission_ranges.cap,
                        ),
                    ],
                ),
                tracer,
            )
