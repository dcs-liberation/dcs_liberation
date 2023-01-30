from dcs.point import MovingPoint
from dcs.task import ActivateBeaconCommand, RecoveryTanker

from game.ato import FlightType
from game.utils import feet, knots
from .pydcswaypointbuilder import PydcsWaypointBuilder


class RecoveryTankerBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:

        assert self.flight.flight_type == FlightType.REFUELING
        group_id = self._get_carrier_group_id()
        speed = knots(250).meters_per_second
        altitude = feet(6000).meters

        # Last waypoint has index of 1.
        # Give the tanker a end condition of the last carrier waypoint.
        # If the carrier ever gets more than one waypoint this approach needs to change.
        last_waypoint = 2
        recovery_tanker = RecoveryTanker(group_id, speed, altitude, last_waypoint)

        waypoint.add_task(recovery_tanker)

        self.configure_tanker_tacan(waypoint)

    def _get_carrier_group_id(self) -> int:
        name = self.package.target.name
        carrier_position = self.package.target.position
        theater_objects = self.unit_map.theater_objects
        for key, value in theater_objects.items():
            # Check name and position in case there are multiple of same carrier.
            if name in key and value.theater_unit.position == carrier_position:
                return value.dcs_group_id
        raise RuntimeError(
            f"Could not find a carrier in the mission matching {name} at "
            f"({carrier_position.x}, {carrier_position.y})"
        )

    def configure_tanker_tacan(self, waypoint: MovingPoint) -> None:

        if self.flight.unit_type.dcs_unit_type.tacan:
            tanker_info = self.mission_data.tankers[-1]
            tacan = tanker_info.tacan
            tacan_callsign = {
                "Texaco": "TEX",
                "Arco": "ARC",
                "Shell": "SHL",
            }.get(tanker_info.callsign)

            waypoint.add_task(
                ActivateBeaconCommand(
                    tacan.number,
                    tacan.band.value,
                    tacan_callsign,
                    bearing=True,
                    unit_id=self.group.units[0].id,
                    aa=True,
                )
            )
