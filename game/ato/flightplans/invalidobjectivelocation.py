from __future__ import annotations

from game.ato import FlightType
from game.ato.flightplans.planningerror import PlanningError
from game.theater import MissionTarget


class InvalidObjectiveLocation(PlanningError):
    """Raised when the objective location is invalid for the mission type."""

    def __init__(self, task: FlightType, location: MissionTarget) -> None:
        super().__init__(f"{location.name} is not valid for {task} missions.")
