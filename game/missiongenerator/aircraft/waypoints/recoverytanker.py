from dcs.point import MovingPoint
from dcs.task import RecoveryTanker

from game.ato import FlightType
from game.utils import feet
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RecoveryTankerBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self.flight.flight_type == FlightType.REFUELING:
            group_id = self._get_carrier_group_id()
            speed = 280
            altitude = feet(6000).meters
            last_waypoint = 1
            recovery_tanker = RecoveryTanker(group_id, speed, altitude, last_waypoint)

            waypoint.add_task(recovery_tanker)

    def _get_carrier_group_id(self) -> int:
        name = self.package.target.name
        carrier_position = self.package.target.position
        theater_objects = self.unit_map.theater_objects
        for key, value in theater_objects.items():
            # Check name and position in case there are multiple of same carrier.
            if name in key and value.theater_unit.position == carrier_position:
                theater_mapping = value
                break
        assert theater_mapping is not None
        return theater_mapping.dcs_unit.id
