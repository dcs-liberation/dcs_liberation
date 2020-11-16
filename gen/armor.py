from __future__ import annotations
import logging
import random
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from dcs import Mission
from dcs.action import AITaskPush
from dcs.condition import GroupLifeLess, Or, TimeAfter, UnitDamaged
from dcs.country import Country
from dcs.mapping import Point
from dcs.planes import MQ_9_Reaper
from dcs.point import PointAction
from dcs.task import (
    AttackGroup,
    ControlledTask,
    EPLRS,
    FireAtPoint,
    GoToWaypoint,
    Hold,
    OrbitAction,
    SetImmortalCommand,
    SetInvisibleCommand,
)
from dcs.triggers import Event, TriggerOnce
from dcs.unit import Vehicle
from dcs.unittype import VehicleType

from game import db
from .naming import namegen
from gen.ground_forces.ai_ground_planner import (
    CombatGroupRole,
    DISTANCE_FROM_FRONTLINE,
)
from .callsigns import callsign_for_support_unit
from .conflictgen import Conflict
from .ground_forces.combat_stance import CombatStance
from game.plugins import LuaPluginManager

if TYPE_CHECKING:
    from game import Game

SPREAD_DISTANCE_FACTOR = 0.1, 0.3
SPREAD_DISTANCE_SIZE_FACTOR = 0.1

FRONTLINE_CAS_FIGHTS_COUNT = 16, 24
FRONTLINE_CAS_GROUP_MIN = 1, 2
FRONTLINE_CAS_PADDING = 12000

RETREAT_DISTANCE = 20000
BREAKTHROUGH_OFFENSIVE_DISTANCE = 35000
AGGRESIVE_MOVE_DISTANCE = 16000

FIGHT_DISTANCE = 3500

RANDOM_OFFSET_ATTACK = 250


@dataclass(frozen=True)
class JtacInfo:
    """JTAC information."""
    dcsGroupName: str
    unit_name: str
    callsign: str
    region: str
    code: str
    # TODO: Radio info? Type?


class GroundConflictGenerator:

    def __init__(self, mission: Mission, conflict: Conflict, game: Game, player_planned_combat_groups, enemy_planned_combat_groups, player_stance):
        self.mission = mission
        self.conflict = conflict
        self.enemy_planned_combat_groups = enemy_planned_combat_groups
        self.player_planned_combat_groups = player_planned_combat_groups
        self.player_stance = CombatStance(player_stance)
        self.enemy_stance = random.choice([CombatStance.AGGRESSIVE, CombatStance.AGGRESSIVE, CombatStance.AGGRESSIVE, CombatStance.ELIMINATION, CombatStance.BREAKTHROUGH]) if len(enemy_planned_combat_groups) > len(player_planned_combat_groups) else random.choice([CombatStance.DEFENSIVE, CombatStance.DEFENSIVE, CombatStance.DEFENSIVE, CombatStance.AMBUSH, CombatStance.AGGRESSIVE])
        self.game = game
        self.jtacs: List[JtacInfo] = []

    def _group_point(self, point) -> Point:
        distance = random.randint(
                int(self.conflict.size * SPREAD_DISTANCE_FACTOR[0]),
                int(self.conflict.size * SPREAD_DISTANCE_FACTOR[1]),
                )
        return point.random_point_within(distance, self.conflict.size * SPREAD_DISTANCE_SIZE_FACTOR)

    def generate(self):

        player_groups = []
        enemy_groups = []

        combat_width = self.conflict.distance/2
        if combat_width > 500000:
            combat_width = 500000
        if combat_width < 35000:
            combat_width = 35000

        position = Conflict.frontline_position(self.conflict.from_cp, self.conflict.to_cp, self.game.theater)

        # Create player groups at random position
        for group in self.player_planned_combat_groups:
            if group.role == CombatGroupRole.ARTILLERY:
                distance_from_frontline = self.get_artilery_group_distance_from_frontline(group)
            else:
                distance_from_frontline = DISTANCE_FROM_FRONTLINE[group.role]
            final_position = self.get_valid_position_for_group(position, True, combat_width, distance_from_frontline)

            if final_position is not None:
                g = self._generate_group(
                    side=self.mission.country(self.game.player_country),
                    unit=group.units[0],
                    heading=self.conflict.heading+90,
                    count=len(group.units),
                    at=final_position)
                g.set_skill(self.game.settings.player_skill)
                player_groups.append((g,group))

                self.gen_infantry_group_for_group(g, True, self.mission.country(self.game.player_country), self.conflict.heading + 90)
            else:
                logging.warning(f"Unable to get valid position for {group}")

        # Create enemy groups at random position
        for group in self.enemy_planned_combat_groups:
            if group.role == CombatGroupRole.ARTILLERY:
                distance_from_frontline = self.get_artilery_group_distance_from_frontline(group)
            else:
                distance_from_frontline = DISTANCE_FROM_FRONTLINE[group.role]
            final_position = self.get_valid_position_for_group(position, False, combat_width, distance_from_frontline)

            if final_position is not None:
                g = self._generate_group(
                    side=self.mission.country(self.game.enemy_country),
                    unit=group.units[0],
                    heading=self.conflict.heading - 90,
                    count=len(group.units),
                    at=final_position)
                g.set_skill(self.game.settings.enemy_vehicle_skill)
                enemy_groups.append((g, group))

                self.gen_infantry_group_for_group(g, False, self.mission.country(self.game.enemy_country), self.conflict.heading - 90)

        # Plan combat actions for groups
        self.plan_action_for_groups(self.player_stance, player_groups, enemy_groups, self.conflict.heading + 90, self.conflict.from_cp, self.conflict.to_cp)
        self.plan_action_for_groups(self.enemy_stance, enemy_groups, player_groups, self.conflict.heading - 90, self.conflict.to_cp, self.conflict.from_cp)

        # Add JTAC
        if self.game.player_faction.has_jtac:
            n = "JTAC" + str(self.conflict.from_cp.id) + str(self.conflict.to_cp.id)
            code = 1688 - len(self.jtacs)

            utype = MQ_9_Reaper
            if self.game.player_faction.jtac_unit is not None:
                utype = self.game.player_faction.jtac_unit

            jtac = self.mission.flight_group(country=self.mission.country(self.game.player_country),
                                             name=n,
                                             aircraft_type=utype,
                                             position=position[0],
                                             airport=None,
                                             altitude=5000)
            jtac.points[0].tasks.append(SetInvisibleCommand(True))
            jtac.points[0].tasks.append(SetImmortalCommand(True))
            jtac.points[0].tasks.append(OrbitAction(5000, 300, OrbitAction.OrbitPattern.Circle))
            frontline = f"Frontline {self.conflict.from_cp.name}/{self.conflict.to_cp.name}"
            # Note: Will need to change if we ever add ground based JTAC.
            callsign = callsign_for_support_unit(jtac)
            self.jtacs.append(JtacInfo(str(jtac.name), n, callsign, frontline, str(code)))

    def gen_infantry_group_for_group(self, group, is_player, side:Country, forward_heading):

        # Disable infantry unit gen if disabled
        if not self.game.settings.perf_infantry:
            return

        infantry_position = group.points[0].position.random_point_within(250, 50)

        if side == self.conflict.attackers_country:
            cp = self.conflict.from_cp
        else:
            cp = self.conflict.to_cp

        if is_player:
            faction = self.game.player_name
        else:
            faction = self.game.enemy_name

        possible_infantry_units = db.find_infantry(faction)
        if len(possible_infantry_units) == 0:
            return

        u = random.choice(possible_infantry_units)
        self.mission.vehicle_group(
                side,
                namegen.next_infantry_name(side, cp, u), u,
                position=infantry_position,
                group_size=1,
                heading=forward_heading,
                move_formation=PointAction.OffRoad)

        for i in range(random.randint(3, 10)):
            u = random.choice(possible_infantry_units)
            position = infantry_position.random_point_within(55, 5)
            self.mission.vehicle_group(
                side,
                namegen.next_infantry_name(side, cp, u), u,
                position=position,
                group_size=1,
                heading=forward_heading,
                move_formation=PointAction.OffRoad)


    def plan_action_for_groups(self, stance, ally_groups, enemy_groups, forward_heading, from_cp, to_cp):

        if not self.game.settings.perf_moving_units:
            return

        for dcs_group, group in ally_groups:

            if hasattr(group.units[0], 'eplrs'):
                if group.units[0].eplrs:
                    dcs_group.points[0].tasks.append(EPLRS(dcs_group.id))

            if group.role == CombatGroupRole.ARTILLERY:
                # Fire on any ennemy in range
                if self.game.settings.perf_artillery:
                    target = self.get_artillery_target_in_range(dcs_group, group, enemy_groups)
                    if target is not None:

                        if stance != CombatStance.RETREAT:
                            hold_task = Hold()
                            hold_task.number = 1
                            dcs_group.add_trigger_action(hold_task)

                        # Artillery strike random start
                        artillery_trigger = TriggerOnce(Event.NoEvent, "ArtilleryFireTask #" + str(dcs_group.id))
                        artillery_trigger.add_condition(TimeAfter(seconds=random.randint(1, 45)* 60))

                        fire_task = FireAtPoint(target, len(group.units) * 10, 100)
                        if stance != CombatStance.RETREAT:
                            fire_task.number = 2
                        else:
                            fire_task.number = 1
                        dcs_group.add_trigger_action(fire_task)
                        artillery_trigger.add_action(AITaskPush(dcs_group.id, len(dcs_group.tasks)))
                        self.mission.triggerrules.triggers.append(artillery_trigger)

                        # Artillery will fall back when under attack
                        if stance != CombatStance.RETREAT:

                            # Hold position
                            dcs_group.points[0].tasks.append(Hold())
                            retreat = self.find_retreat_point(dcs_group, forward_heading, (int)(RETREAT_DISTANCE/3))
                            dcs_group.add_waypoint(dcs_group.position.point_from_heading(forward_heading, 1), PointAction.OffRoad)
                            dcs_group.points[1].tasks.append(Hold())
                            dcs_group.add_waypoint(retreat, PointAction.OffRoad)

                            artillery_fallback = TriggerOnce(Event.NoEvent, "ArtilleryRetreat #" + str(dcs_group.id))
                            for i, u in enumerate(dcs_group.units):
                                artillery_fallback.add_condition(UnitDamaged(u.id))
                                if i < len(dcs_group.units) - 1:
                                    artillery_fallback.add_condition(Or())

                            hold_2 = Hold()
                            hold_2.number = 3
                            dcs_group.add_trigger_action(hold_2)

                            retreat_task = GoToWaypoint(toIndex=3)
                            retreat_task.number = 4
                            dcs_group.add_trigger_action(retreat_task)

                            artillery_fallback.add_action(AITaskPush(dcs_group.id, len(dcs_group.tasks)))
                            self.mission.triggerrules.triggers.append(artillery_fallback)

                            for u in dcs_group.units:
                                u.initial = True
                                u.heading = forward_heading + random.randint(-5,5)

            elif group.role in [CombatGroupRole.TANK, CombatGroupRole.IFV]:
                if stance == CombatStance.AGGRESSIVE:
                    # Attack nearest enemy if any
                    # Then move forward OR Attack enemy base if it is not too far away
                    target = self.find_nearest_enemy_group(dcs_group, enemy_groups)
                    if target is not None:
                        rand_offset = Point(random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK), random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK))
                        dcs_group.add_waypoint(target.points[0].position + rand_offset, PointAction.OffRoad)
                        dcs_group.points[1].tasks.append(AttackGroup(target.id))

                    if to_cp.position.distance_to_point(dcs_group.points[0].position) <= AGGRESIVE_MOVE_DISTANCE:
                        attack_point = to_cp.position.random_point_within(500, 0)
                    else:
                        attack_point = self.find_offensive_point(dcs_group, forward_heading, AGGRESIVE_MOVE_DISTANCE)
                    dcs_group.add_waypoint(attack_point, PointAction.OnRoad)
                elif stance == CombatStance.BREAKTHROUGH:
                    # In breakthrough mode, the units will move forward
                    # If the enemy base is close enough, the units will attack the base
                    if to_cp.position.distance_to_point(
                            dcs_group.points[0].position) <= BREAKTHROUGH_OFFENSIVE_DISTANCE:
                        attack_point = to_cp.position.random_point_within(500, 0)
                    else:
                        attack_point = self.find_offensive_point(dcs_group, forward_heading, BREAKTHROUGH_OFFENSIVE_DISTANCE)
                    dcs_group.add_waypoint(attack_point, PointAction.OnRoad)
                elif stance == CombatStance.ELIMINATION:
                    # In elimination mode, the units focus on destroying as much enemy groups as possible
                    targets = self.find_n_nearest_enemy_groups(dcs_group, enemy_groups, 3)
                    i = 1
                    for target in targets:
                        rand_offset = Point(random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK), random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK))
                        dcs_group.add_waypoint(target.points[0].position+rand_offset, PointAction.OffRoad)
                        dcs_group.points[i].tasks.append(AttackGroup(target.id))
                        i = i + 1
                    if to_cp.position.distance_to_point(dcs_group.points[0].position) <= AGGRESIVE_MOVE_DISTANCE:
                        attack_point = to_cp.position.random_point_within(500, 0)
                        dcs_group.add_waypoint(attack_point)

                if stance != CombatStance.RETREAT:
                    self.add_morale_trigger(dcs_group, forward_heading)

            elif group.role in [CombatGroupRole.APC, CombatGroupRole.ATGM]:

                if stance in [CombatStance.AGGRESSIVE, CombatStance.BREAKTHROUGH, CombatStance.ELIMINATION]:
                    # APC & ATGM will never move too much forward, but will follow along any offensive
                    if to_cp.position.distance_to_point(dcs_group.points[0].position) <= AGGRESIVE_MOVE_DISTANCE:
                        attack_point = to_cp.position.random_point_within(500, 0)
                    else:
                        attack_point = self.find_offensive_point(dcs_group, forward_heading, AGGRESIVE_MOVE_DISTANCE)
                    dcs_group.add_waypoint(attack_point, PointAction.OnRoad)

                if stance != CombatStance.RETREAT:
                    self.add_morale_trigger(dcs_group, forward_heading)

            if stance == CombatStance.RETREAT:
                # In retreat mode, the units will fall back
                # If the ally base is close enough, the units will even regroup there
                if from_cp.position.distance_to_point(dcs_group.points[0].position) <= RETREAT_DISTANCE:
                    retreat_point = from_cp.position.random_point_within(500, 250)
                else:
                    retreat_point = self.find_retreat_point(dcs_group, forward_heading)
                reposition_point = retreat_point.point_from_heading(forward_heading, 10)  # Another point to make the unit face the enemy
                dcs_group.add_waypoint(retreat_point, PointAction.OnRoad)
                dcs_group.add_waypoint(reposition_point, PointAction.OffRoad)


    def add_morale_trigger(self, dcs_group, forward_heading):
        """
        This add a trigger to manage units fleeing whenever their group is hit hard, or being engaged by CAS
        """

        if len(dcs_group.units) == 1:
            return

        # Units should hold position on last waypoint
        dcs_group.points[len(dcs_group.points) - 1].tasks.append(Hold())

        # Force unit heading
        for unit in dcs_group.units:
            unit.heading = forward_heading
        dcs_group.manualHeading = True

        # We add a new retreat waypoint
        dcs_group.add_waypoint(self.find_retreat_point(dcs_group, forward_heading, (int)(RETREAT_DISTANCE / 8)), PointAction.OffRoad)

        # Fallback task
        fallback = ControlledTask(GoToWaypoint(toIndex=len(dcs_group.points)))
        fallback.enabled = False
        dcs_group.add_trigger_action(Hold())
        dcs_group.add_trigger_action(fallback)

        # Create trigger
        fallback = TriggerOnce(Event.NoEvent, "Morale manager #" + str(dcs_group.id))

        # Usually more than 50% casualties = RETREAT
        fallback.add_condition(GroupLifeLess(dcs_group.id, random.randint(51, 76)))

        # Do retreat to the configured retreat waypoint
        fallback.add_action(AITaskPush(dcs_group.id, len(dcs_group.tasks)))

        self.mission.triggerrules.triggers.append(fallback)


    def find_retreat_point(self, dcs_group, frontline_heading, distance=RETREAT_DISTANCE):
        """
        Find a point to retreat to
        :param dcs_group: DCS mission group we are searching a retreat point for
        :param frontline_heading: Heading of the frontline
        :return: dcs.mapping.Point object with the desired position
        """
        return dcs_group.points[0].position.point_from_heading(frontline_heading-180, distance)

    def find_offensive_point(self, dcs_group, frontline_heading, distance):
        """
        Find a point to attack
        :param dcs_group:  DCS mission group we are searching an attack point for
        :param frontline_heading: Heading of the frontline
        :param distance: Distance of the offensive (how far unit should move)
        :return: dcs.mapping.Point object with the desired position
        """
        return dcs_group.points[0].position.point_from_heading(frontline_heading, distance)

    def find_n_nearest_enemy_groups(self, player_group, enemy_groups, n):
        """
        Return the neaarest enemy group for the player group
        @param group Group for which we should find the nearest ennemies
        @param enemy_groups Potential enemy groups
        @param n number of nearby groups to take
        """
        targets = []
        sorted_list = sorted(enemy_groups, key=lambda group: player_group.points[0].position.distance_to_point(group[0].points[0].position))
        for i in range(n):
            if len(sorted_list) <= i:
                break
            else:
                targets.append(sorted_list[i][0])
        return targets


    def find_nearest_enemy_group(self, player_group, enemy_groups):
        """
        Search the enemy groups for a potential target suitable to armored assault
        @param group Group for which we should find the nearest ennemy
        @param enemy_groups Potential enemy groups
        """
        min_distance = 99999999
        target = None
        for dcs_group, group in enemy_groups:
            dist = player_group.points[0].position.distance_to_point(dcs_group.points[0].position)
            if dist < min_distance:
                min_distance = dist
                target = dcs_group
        return target


    def get_artillery_target_in_range(self, dcs_group, group, enemy_groups):
        """
        Search the enemy groups for a potential target suitable to an artillery unit
        """
        rng = group.units[0].threat_range
        if len(enemy_groups) == 0:
            return None
        for o in range(10):
            potential_target = random.choice(enemy_groups)[0]
            distance_to_target = dcs_group.points[0].position.distance_to_point(potential_target.points[0].position)
            if distance_to_target < rng:
                return potential_target.points[0].position
        return None


    def get_artilery_group_distance_from_frontline(self, group):
        """
        For artilery group, decide the distance from frontline with the range of the unit
        """
        rg = group.units[0].threat_range - 7500
        if rg > DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY]:
            rg = DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY]
        if rg < DISTANCE_FROM_FRONTLINE[CombatGroupRole.TANK]:
            rg = DISTANCE_FROM_FRONTLINE[CombatGroupRole.TANK] + 100
        return rg


    def get_valid_position_for_group(self, conflict_position, isplayer, combat_width, distance_from_frontline):
        i = 0
        while i < 1000: # 25 attempt for valid position
            heading_diff = -90 if isplayer else 90
            shifted = conflict_position[0].point_from_heading(self.conflict.heading,
                                                     random.randint((int)(-combat_width / 2), (int)(combat_width / 2)))
            final_position = shifted.point_from_heading(self.conflict.heading + heading_diff, distance_from_frontline)

            if self.conflict.theater.is_on_land(final_position):
                return final_position
            else:
                i = i + 1
                continue
        return None

    def _generate_group(self, side: Country, unit: VehicleType, count: int, at: Point, move_formation: PointAction = PointAction.OffRoad, heading=0):

        if side == self.conflict.attackers_country:
            cp = self.conflict.from_cp
        else:
            cp = self.conflict.to_cp

        logging.info("armorgen: {} for {}".format(unit, side.id))
        group = self.mission.vehicle_group(
                side,
                namegen.next_unit_name(side, cp.id, unit), unit,
                position=self._group_point(at),
                group_size=count,
                heading=heading,
                move_formation=move_formation)

        for c in range(count):
            vehicle: Vehicle = group.units[c]
            vehicle.player_can_drive = True

        return group