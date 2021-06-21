from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Generic, TypeVar

from game.commander.missionproposals import ProposedFlight, EscortType, ProposedMission
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.htn import PrimitiveTask
from game.profiling import MultiEventTracer
from game.theater import MissionTarget
from game.utils import Distance
from gen.flights.flight import FlightType

if TYPE_CHECKING:
    from gen.flights.ai_flight_planner import CoalitionMissionPlanner


MissionTargetT = TypeVar("MissionTargetT", bound=MissionTarget)


# TODO: Refactor so that we don't need to call up to the mission planner.
# Bypass type checker due to https://github.com/python/mypy/issues/5374
@dataclass  # type: ignore
class PackagePlanningTask(PrimitiveTask[TheaterState], Generic[MissionTargetT]):
    target: MissionTargetT
    flights: list[ProposedFlight] = field(init=False)

    def __post_init__(self) -> None:
        self.flights = []

    def execute(
        self, mission_planner: CoalitionMissionPlanner, tracer: MultiEventTracer
    ) -> None:
        self.propose_flights(mission_planner.doctrine)
        mission_planner.plan_mission(ProposedMission(self.target, self.flights), tracer)

    @abstractmethod
    def propose_flights(self, doctrine: Doctrine) -> None:
        ...

    def propose_flight(
        self,
        task: FlightType,
        num_aircraft: int,
        max_distance: Optional[Distance],
        escort_type: Optional[EscortType] = None,
    ) -> None:
        if max_distance is None:
            max_distance = Distance.inf()
        self.flights.append(
            ProposedFlight(task, num_aircraft, max_distance, escort_type)
        )

    @property
    def asap(self) -> bool:
        return False

    def propose_common_escorts(self, doctrine: Doctrine) -> None:
        self.propose_flight(
            FlightType.SEAD_ESCORT,
            2,
            doctrine.mission_ranges.offensive,
            EscortType.Sead,
        )

        self.propose_flight(
            FlightType.ESCORT,
            2,
            doctrine.mission_ranges.offensive,
            EscortType.AirToAir,
        )
