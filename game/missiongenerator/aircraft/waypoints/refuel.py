from dcs.point import MovingPoint, PointAction
from dcs.task import OptRestrictAfterburner, Refueling, RefuelingTaskAction
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    # num_aircraft: int = 0

    # for flight in self.package:
    #     for element in flight:
    #         # TODO: determine if aircraft can be refueled so that it can be counted
    #         num_aircraft+=1

    # self.elapsed_mission_time = 60 * (self.package.flights.count + num_aircraft * 3);

    def add_tasks(self, waypoint: MovingPoint) -> None:
        waypoint.add_task(RefuelingTaskAction())
        waypoint.add_task(OptRestrictAfterburner(value=True))
        return super().add_tasks(waypoint)
