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
            # Should this be an enum?
            target_types = ["Ships"]
            last_waypoint = None
            recovery_tanker = RecoveryTanker(
                group_id, speed, altitude, target_types, last_waypoint
            )

            waypoint.add_task(recovery_tanker)

    def _get_carrier_group_id(self) -> int:
        name = self.package.target.name
        theater_mapping = self.unit_map.theater_objects.get(name)
        assert theater_mapping is not None
        return theater_mapping.dcs_unit.id
