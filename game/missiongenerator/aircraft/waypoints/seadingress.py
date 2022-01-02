import logging

from dcs.point import MovingPoint
from dcs.task import AttackGroup, OptECMUsing, WeaponType

from game.theater import TheaterGroundObject
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SeadIngressBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:
        self.register_special_waypoints(self.waypoint.targets)

        target = self.package.target
        if not isinstance(target, TheaterGroundObject):
            logging.error(
                "Unexpected target type for SEAD mission: %s",
                target.__class__.__name__,
            )
            return

        for group in target.groups:
            miz_group = self.mission.find_group(group.name)
            if miz_group is None:
                logging.error(f"Could not find group for SEAD mission {group.name}")
                continue

            task = AttackGroup(miz_group.id, weapon_type=WeaponType.Guided)
            task.params["expend"] = "All"
            task.params["attackQtyLimit"] = False
            task.params["directionEnabled"] = False
            task.params["altitudeEnabled"] = False
            task.params["groupAttack"] = True
            waypoint.tasks.append(task)

        # Preemptively use ECM to better avoid getting swatted.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)
