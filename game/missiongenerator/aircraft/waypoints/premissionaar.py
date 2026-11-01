from dcs.point import MovingPoint
from dcs.task import RefuelingTaskAction

from game.ato import FlightType
from .pydcswaypointbuilder import PydcsWaypointBuilder


class PreMissionAarBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self._has_refueling_available():
            waypoint.add_task(RefuelingTaskAction())
        return super().add_tasks(waypoint)

    def _has_refueling_available(self) -> bool:
        if self.package.has_flight_with_task(FlightType.REFUELING):
            return True
        ato = getattr(self.flight.coalition, "ato", None)
        for package in getattr(ato, "packages", []):
            if package.has_flight_with_task(FlightType.REFUELING):
                return True
        return False
