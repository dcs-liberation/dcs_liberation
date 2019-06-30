import typing
import random
from datetime import datetime, timedelta, time

from dcs.mission import Mission
from dcs.triggers import *
from dcs.condition import *
from dcs.action import *
from dcs.unit import Skill
from dcs.point import MovingPoint, PointProperties
from dcs.action import *

from game import db
from theater import *
from gen.airsupportgen import AirSupportConflictGenerator
from gen import *

PUSH_TRIGGER_SIZE = 3000
PUSH_TRIGGER_ACTIVATION_AGL = 25

REGROUP_ZONE_DISTANCE = 12000
REGROUP_ALT = 5000

TRIGGER_WAYPOINT_OFFSET = 2
TRIGGER_MIN_DISTANCE_FROM_START = 10000
# modified since we now have advanced SAM units
TRIGGER_RADIUS_MINIMUM = 3000000

TRIGGER_RADIUS_SMALL = 50000
TRIGGER_RADIUS_MEDIUM = 100000
TRIGGER_RADIUS_LARGE = 150000
TRIGGER_RADIUS_ALL_MAP = 3000000


class Silence(Option):
    Key = 7


class TriggersGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.mission = mission
        self.conflict = conflict
        self.game = game

    def _gen_activation_trigger(self, radius: int, player_cp: ControlPoint, player_coalition: str, enemy_coalition: str):
        conflict_distance = player_cp.position.distance_to_point(self.conflict.position)
        minimum_radius = max(conflict_distance - TRIGGER_MIN_DISTANCE_FROM_START, TRIGGER_RADIUS_MINIMUM)
        if minimum_radius < 0:
            minimum_radius = 0
        radius = min(minimum_radius, radius)
        activation_trigger_zone = self.mission.triggers.add_triggerzone(
            self.conflict.position,
            radius,
            name="Activation zone",
        )
        activation_trigger = TriggerOnce(Event.NoEvent, "Activation trigger")
        activation_trigger.add_condition(PartOfCoalitionInZone(player_coalition, activation_trigger_zone.id))
        activation_trigger.add_condition(FlagIsTrue())
        activate_by_trigger = []
        flag_id = 2
        for coalition_name, coalition in self.mission.coalition.items():
            for country in coalition.countries.values():
                if coalition_name == enemy_coalition:
                    for plane_group in country.plane_group + country.helicopter_group:
                        plane_group.late_activation = True
                        self.delayed_trigger(
                            plane_group,
                            flag_id,
                            flag_lower_limit=180,
                            flag_upper_limit=2400,
                        )
                        flag_id += 1

                for vehicle_group in country.vehicle_group:
                    vehicle_group.late_activation = True
                    activate_by_trigger.append(vehicle_group)

        for group in activate_by_trigger:
            activation_trigger.add_action(ActivateGroup(group.id))

        self.mission.triggerrules.triggers.append(activation_trigger)

    def _gen_push_trigger(self, player_cp: ControlPoint, player_coalition: str):
        push_by_trigger = []
        for coalition_name, coalition in self.mission.coalition.items():
            for country in coalition.countries.values():
                if coalition_name == player_coalition:
                    for group in country.plane_group + country.helicopter_group:
                        if group.task == AWACS.name or group.task == Refueling.name:
                            continue

                        push_by_trigger.append(group)

                        if not group.units[0].is_human():
                            regroup_heading = self.conflict.to_cp.position.heading_between_point(player_cp.position)

                            pos1 = group.position.point_from_heading(regroup_heading, REGROUP_ZONE_DISTANCE)
                            pos2 = group.position.point_from_heading(regroup_heading, REGROUP_ZONE_DISTANCE+5000)
                            w1 = group.add_waypoint(pos1, REGROUP_ALT)
                            w2 = group.add_waypoint(pos2, REGROUP_ALT)

                            group.points.remove(w1)
                            group.points.remove(w2)

                            group.points.insert(1, w2)
                            group.points.insert(1, w1)

                            w1.tasks.append(Silence(True))

                            switch_waypoint_task = ControlledTask(SwitchWaypoint(from_waypoint=3, to_waypoint=2))
                            switch_waypoint_task.start_if_user_flag(1, False)
                            w2.tasks.append(switch_waypoint_task)
                            group.points[3].tasks.append(Silence(False))

                            group.add_trigger_action(SwitchWaypoint(to_waypoint=4))

        push_trigger = TriggerOnce(Event.NoEvent, "Push trigger")

        for group in push_by_trigger:
            for unit in group.units:
                push_trigger.add_condition(UnitAltitudeHigherAGL(unit.id, PUSH_TRIGGER_ACTIVATION_AGL))

            if not group.units[0].is_human():
                push_trigger.add_action(AITaskPush(group.id, 1))

        message_string = self.mission.string("Task force is in the air, proceed with the objective.")
        push_trigger.add_action(MessageToAll(message_string, clearview=True))
        push_trigger.add_action(SetFlagValue())

        self.mission.triggerrules.triggers.append(push_trigger)

    def _set_allegiances(self, player_coalition: str, enemy_coalition: str):
        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue
            self.mission.terrain.airport_by_id(cp.at.id).set_coalition(cp.captured and player_coalition or enemy_coalition)

    def _set_skill(self, player_coalition: str, enemy_coalition: str):
        for coalition_name, coalition in self.mission.coalition.items():
            if coalition_name == player_coalition:
                skill_level = self.game.settings.player_skill, self.game.settings.player_skill
            elif coalition_name == enemy_coalition:
                skill_level = self.game.settings.enemy_skill, self.game.settings.enemy_vehicle_skill
            else:
                continue

            for country in coalition.countries.values():
                for plane_group in country.plane_group:
                    for plane_unit in plane_group.units:
                        if plane_unit.skill != Skill.Client and plane_unit.skill != Skill.Player:
                            plane_unit.skill = Skill(skill_level[0])

                for vehicle_group in country.vehicle_group:
                    vehicle_group.set_skill(Skill(skill_level[1]))

    def delayed_trigger(self, group, flag_id, flag_lower_limit, flag_upper_limit):
        """
        Create an activation trigger a randomized amount after the main activation occurs
        :param group:
            group to activate
        :param flag_id:
            ID of the flag to use
        :param flag_lower_limit:
            lower limit of what the random time can be (shouldn't be negative)
        :param flag_upper_limit:
            uopper limit of what the random time can be
        :return:
            N/A
        """
        trigger_one = TriggerOnce(Event.NoEvent, "Activation trigger")
        trigger_one.add_condition(FlagEquals(1, 1))
        trigger_one.add_action(SetFlagValue(flag_id, 1))

        trigger_two = TriggerCondition()
        trigger_two.add_condition(
            TimeSinceFlag(
                flag_id,
                seconds=random.randint(
                    flag_lower_limit,
                    flag_upper_limit
                )
            )
        )
        trigger_two.add_action(ActivateGroup(group.id))

        self.mission.triggerrules.triggers.append(trigger_one)
        self.mission.triggerrules.triggers.append(trigger_two)

    def generate(self, player_cp: ControlPoint, is_quick: bool, activation_trigger_radius: int, awacs_enabled: bool):
        player_coalition = self.game.player == "USA" and "blue" or "red"
        enemy_coalition = player_coalition == "blue" and "red" or "blue"

        self.mission.coalition[player_coalition].bullseye = {"x": self.conflict.position.x,
                                                             "y": self.conflict.position.y}

        self._set_skill(player_coalition, enemy_coalition)
        self._set_allegiances(player_coalition, enemy_coalition)

        if not is_quick:
            # TODO: waypoint parts of this should not be post-hacked but added in airgen
            self._gen_activation_trigger(activation_trigger_radius, player_cp, player_coalition, enemy_coalition)
            self._gen_push_trigger(player_cp, player_coalition)

