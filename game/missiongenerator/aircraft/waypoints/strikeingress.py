import copy

from dcs import Point
from dcs.planes import B_17G, B_52H, Tu_22M3
from dcs.point import MovingPoint
from dcs.task import Bombing, Expend, OptFormation, WeaponType

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

        center: Point = copy.copy(targets[0].position)
        for target in targets[1:]:
            center += target.position
        center /= len(targets)
        bombing = Bombing(
            center, weapon_type=WeaponType.Bombs, expend=Expend.All, group_attack=True
        )
        waypoint.tasks.append(bombing)

    def add_strike_tasks(self, waypoint: MovingPoint) -> None:
        for target in self.waypoint.targets:
            bombing = Bombing(
                target.position, weapon_type=WeaponType.Auto, group_attack=True
            )
            # If there is only one target, drop all ordnance in one pass.
            if len(self.waypoint.targets) == 1:
                bombing.params["expend"] = Expend.All.value
            waypoint.tasks.append(bombing)

            # Register special waypoints
            self.register_special_waypoints(self.waypoint.targets)
