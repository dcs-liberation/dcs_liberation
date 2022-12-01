from dcs.point import MovingPoint
from dcs.task import RecoveryTanker

from game.ato import FlightType
from game.utils import feet
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RecoveryTankerBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self.flight.flight_type == FlightType.REFUELING:
            group_id = 1
            speed = 280
            altitude = feet(6000).meters
            target_types = ["huh?"]
            last_waypoint = 2
            recovery_tanker = RecoveryTanker(
                group_id, speed, altitude, target_types, last_waypoint
            )

            waypoint.add_task(recovery_tanker)
