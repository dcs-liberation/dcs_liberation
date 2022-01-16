from dcs import Point
from dcs.planes import B_17G, B_52H, Tu_22M3
from dcs.point import MovingPoint
from dcs.task import Bombing, OptFormation, WeaponType

from .pydcswaypointbuilder import PydcsWaypointBuilder


class StrikeIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        if self.group.units[0].unit_type in [B_17G, B_52H, Tu_22M3]:
            self.add_bombing_tasks(waypoint)
        else:
            self.add_strike_tasks(waypoint)

        waypoint.tasks.append(OptFormation.trail_open())

    def add_bombing_tasks(self, waypoint: MovingPoint) -> None:
        targets = self.waypoint.targets
        if not targets:
            return

        center = Point(0, 0)
        for target in targets:
            center.x += target.position.x
            center.y += target.position.y
        center.x /= len(targets)
        center.y /= len(targets)
        bombing = Bombing(center, weapon_type=WeaponType.Bombs)
        bombing.params["expend"] = "All"
        bombing.params["attackQtyLimit"] = False
        bombing.params["directionEnabled"] = False
        bombing.params["altitudeEnabled"] = False
        bombing.params["groupAttack"] = True
        waypoint.tasks.append(bombing)

    def add_strike_tasks(self, waypoint: MovingPoint) -> None:
        for target in self.waypoint.targets:
            bombing = Bombing(target.position, weapon_type=WeaponType.Auto)
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = "All"
            bombing.params["groupAttack"] = True
            waypoint.tasks.append(bombing)

            # Register special waypoints
            self.register_special_waypoints(self.waypoint.targets)
