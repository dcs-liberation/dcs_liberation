from dcs.point import MovingPoint
from dcs.task import Land

from game.utils import feet
from dcs.point import PointAction


from .pydcswaypointbuilder import PydcsWaypointBuilder


class CargoStopBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        # Create a landing task, currently only for Helos!
        if self.flight.is_helo:
            # Calculate a landing point with a small buffer to prevent AI from landing
            # directly at the static ammo depot and exploding
            landing_point = waypoint.position.random_point_within(15, 5)
            # Use Land Task with 30s duration for helos
            waypoint.add_task(Land(landing_point, duration=30))
        else:
            # Fixed wing will drop the cargo at the waypoint so we set a lower altitude
            waypoint.alt = int(feet(10000).meters)
            waypoint.alt_type = "BARO"
            waypoint.action = PointAction.FlyOverPoint
        return waypoint
