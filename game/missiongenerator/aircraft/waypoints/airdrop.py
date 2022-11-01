from dcs.point import MovingPoint
from dcs.task import Land

from game.utils import feet
from dcs.point import PointAction


from .pydcswaypointbuilder import PydcsWaypointBuilder


class AirDropBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        waypoint = super().build()
        waypoint.alt = int(feet(10000).meters)
        waypoint.alt_type = "BARO"
        waypoint.action = PointAction.FlyOverPoint
        return waypoint
