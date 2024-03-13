from dcs.point import MovingPoint, PointAction

from .pydcswaypointbuilder import PydcsWaypointBuilder


class CargoStopBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "LandingReFuAr"
        waypoint.action = PointAction.LandingReFuAr
        waypoint.landing_refuel_rearm_time = 2  # Minutes.
        if (control_point := self.waypoint.control_point) is not None:
            waypoint.airdrome_id = control_point.airdrome_id_for_landing
        return waypoint
