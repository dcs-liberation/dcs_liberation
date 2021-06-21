from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from game.commander.theaterstate import TheaterState
from game.htn import PrimitiveTask
from game.profiling import MultiEventTracer

if TYPE_CHECKING:
    from gen.flights.ai_flight_planner import CoalitionMissionPlanner


# TODO: Refactor so that we don't need to call up to the mission planner.
class TheaterCommanderTask(PrimitiveTask[TheaterState]):
    @abstractmethod
    def execute(
        self, mission_planner: CoalitionMissionPlanner, tracer: MultiEventTracer
    ) -> None:
        ...
