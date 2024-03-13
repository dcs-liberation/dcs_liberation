from dcs.point import MovingPoint, PointAction

from .pydcswaypointbuilder import PydcsWaypointBuilder


class LandingPointBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.type = "Land"
        waypoint.action = PointAction.Landing
        if (control_point := self.waypoint.control_point) is not None:
            waypoint.airdrome_id = control_point.airdrome_id_for_landing
        return waypoint
