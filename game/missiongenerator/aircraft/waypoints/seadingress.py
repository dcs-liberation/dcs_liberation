import logging

from dcs.point import MovingPoint
from dcs.task import (
    AttackGroup,
    EngageGroup,
    Expend,
    OptECMUsing,
    WeaponType as DcsWeaponType,
)
from game.data.weapons import WeaponType

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
            miz_group = self.mission.find_group(group.group_name)
            if miz_group is None:
                logging.error(
                    f"Could not find group for SEAD mission {group.group_name}"
                )
                continue

            if self.flight.loadout.has_weapon_of_type(WeaponType.ARM):
                # Special handling for ARM Weapon types:
                # The SEAD flight will Search for the targeted group and then engage it
                # if it is found only. This will prevent AI from having huge problems
                # when skynet is enabled and the Radar is not emitting. They dive
                # into the SAM instead of waiting for it to come alive
                engage_task = EngageGroup(miz_group.id)
                engage_task.params["weaponType"] = DcsWeaponType.Guided.value
                engage_task.params["groupAttack"] = True
                engage_task.params["expend"] = Expend.All.value
                waypoint.tasks.append(engage_task)
            else:
                # All non ARM types like Decoys will use the normal AttackGroup Task
                attack_task = AttackGroup(
                    miz_group.id,
                    weapon_type=DcsWeaponType.Guided,
                    group_attack=True,
                    expend=Expend.All,
                )
                waypoint.tasks.append(attack_task)

        # Preemptively use ECM to better avoid getting swatted.
        ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfDetectedLockByRadar)
        waypoint.tasks.append(ecm_option)
