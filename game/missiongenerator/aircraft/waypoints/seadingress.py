import logging

from dcs.point import MovingPoint
from dcs.task import (
    AttackGroup,
    ControlledTask,
    EngageGroup,
    Expend,
    OptECMUsing,
    SwitchWaypoint,
    WeaponType as DcsWeaponType,
)
from game.ato.flightstate import InFlight
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
            elif self.flight.loadout.has_weapon_of_type(WeaponType.DECOY):
                # Special handling for DECOY weapon types:
                # - Specify that DECOY weapon type is used in AttackGroup task so that
                #   the flight actually launches the decoy. See link below for details
                #   https://github.com/dcs-liberation/dcs_liberation/issues/2780
                # - Set a stop condition of 120 seconds so that the flight does not continue
                #   press the engagement as a DCS limitation means the RTB on winchester
                #   does not work well with decoys. See link below for details.
                #   https://github.com/dcs-liberation/dcs_liberation/issues/2781
                #   This stop condition will allow the SwitchWaypoint task defined below
                #   to kick in.
                attack_task = AttackGroup(
                    miz_group.id,
                    weapon_type=DcsWeaponType.Decoy,
                    group_attack=True,
                    expend=Expend.All,
                )
                attack_task_control = ControlledTask(attack_task)
                attack_task_control.stop_after_duration(120)
                waypoint.tasks.append(attack_task_control)
            else:
                # All non ARM and non DECOY types will use the normal AttackGroup Task
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

        # For DECOY type flights, setup a waypoint task to skip the target waypoint after
        # the attack task is complete. This is achieved using a switch waypoint task from the
        # INGRESS point to the SPLIT point. This tasking prevents the flights continuing to
        # overfly the target. See link below for the details of this issue
        # https://github.com/dcs-liberation/dcs_liberation/issues/2781
        if self.flight.loadout.has_weapon_of_type(WeaponType.DECOY):
            switch_waypoint_task = SwitchWaypoint(
                self.generated_waypoint_idx, self.generated_waypoint_idx + 2
            )
            waypoint.tasks.append(switch_waypoint_task)
