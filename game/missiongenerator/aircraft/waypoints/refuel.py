from dcs.point import MovingPoint, PointAction
from dcs.task import Refueling, RefuelingTaskAction
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RefuelPointBuilder(PydcsWaypointBuilder):
    def build(self) -> None:
        self.waypoint = super().build()
        self.waypoint.type = "Refuel"
        self.waypoint.action = PointAction.FlyOverPoint
        self.waypoint.add_task(RefuelingTaskAction)

        # num_aircraft: int = 0

        # for flight in self.package:
        #     for element in flight:
        #         # TODO: determine if aircraft can be refueled so that it can be counted
        #         num_aircraft+=1

        # self.elapsed_mission_time = 60 * (self.package.flights.count + num_aircraft * 3);
