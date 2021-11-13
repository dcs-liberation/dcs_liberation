from dcs.point import MovingPoint
from dcs.task import RefuelingTaskAction
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        waypoint.add_task(RefuelingTaskAction())
        return super().add_tasks(waypoint)
