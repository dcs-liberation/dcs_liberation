from dcs.point import MovingPoint
from dcs.task import Land


from .pydcswaypointbuilder import PydcsWaypointBuilder


class LandingZoneBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        # Create a landing task, currently only for Helos!
        # Calculate a landing point with a small buffer to prevent AI from landing
        # directly at the static ammo depot and exploding
        landing_point = waypoint.position.random_point_within(15, 5)
        # Use Land Task with 30s duration for helos
        waypoint.add_task(Land(landing_point, duration=30))
        return waypoint
