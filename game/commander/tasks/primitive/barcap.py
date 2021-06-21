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

    def preconditions_met(self, state: TheaterState) -> bool:
        return self.target in state.vulnerable_control_points

    def apply_effects(self, state: TheaterState) -> None:
        state.vulnerable_control_points.remove(self.target)

    def execute(
        self, mission_planner: CoalitionMissionPlanner, tracer: MultiEventTracer
    ) -> None:
        # Plan enough rounds of CAP that the target has coverage over the expected
        # mission duration.
        mission_duration = int(
            mission_planner.game.settings.desired_player_mission_duration.total_seconds()
        )
        barcap_duration = int(
            mission_planner.faction.doctrine.cap_duration.total_seconds()
        )
        for _ in range(
            0,
            mission_duration,
            barcap_duration,
        ):
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
