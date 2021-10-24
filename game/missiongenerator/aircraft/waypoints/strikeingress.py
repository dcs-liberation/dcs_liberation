from dcs import Point
from dcs.planes import B_17G, B_52H, Tu_22M3
from dcs.point import MovingPoint
from dcs.task import Bombing, WeaponType

from .pydcswaypointbuilder import PydcsWaypointBuilder


class StrikeIngressBuilder(PydcsWaypointBuilder):
    def build(self) -> MovingPoint:
        if self.group.units[0].unit_type in [B_17G, B_52H, Tu_22M3]:
            return self.build_bombing()
        else:
            return self.build_strike()

    def build_bombing(self) -> MovingPoint:
        waypoint = super().build()

        targets = self.waypoint.targets
        if not targets:
            return waypoint

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
        return waypoint

    def build_strike(self) -> MovingPoint:
        waypoint = super().build()
        for target in self.waypoint.targets:
            bombing = Bombing(target.position, weapon_type=WeaponType.Auto)
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = "All"
            bombing.params["groupAttack"] = True
            waypoint.tasks.append(bombing)

            # Register special waypoints
            self.register_special_waypoints(self.waypoint.targets)
        return waypoint
