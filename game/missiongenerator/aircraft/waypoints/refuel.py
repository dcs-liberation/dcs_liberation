from dcs.point import MovingPoint
from dcs.task import RefuelingTaskAction

from game.ato import FlightType
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self.package.has_flight_with_task(FlightType.REFUELING):
            waypoint.add_task(RefuelingTaskAction())
        return super().add_tasks(waypoint)
