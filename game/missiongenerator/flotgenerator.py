from __future__ import annotations

import math
import random
from typing import List, Optional, TYPE_CHECKING, Tuple

from dcs import Mission
from dcs.action import AITaskPush
from dcs.condition import GroupLifeLess, Or, TimeAfter, UnitDamaged
from dcs.country import Country
from dcs.mapping import Point, Vector2
from dcs.point import PointAction
from dcs.task import (
    AFAC,
    AttackGroup,
    ControlledTask,
    EPLRS,
    FAC,
    FireAtPoint,
    GoToWaypoint,
    Hold,
    OrbitAction,
    SetImmortalCommand,
    SetInvisibleCommand,
)
from dcs.triggers import Event, TriggerOnce
from dcs.unit import Skill, Vehicle
from dcs.unitgroup import VehicleGroup

from game.callsigns import callsign_for_support_unit
from game.data.units import UnitClass
from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.ground_forces.ai_ground_planner import (
    CombatGroup,
    CombatGroupRole,
    DISTANCE_FROM_FRONTLINE,
)
from game.ground_forces.combat_stance import CombatStance
from game.naming import namegen
from game.radio.radios import RadioRegistry
from game.theater.controlpoint import ControlPoint
from game.unitmap import UnitMap
from game.utils import Heading
from .frontlineconflictdescription import FrontLineConflictDescription
from .lasercoderegistry import LaserCodeRegistry
from .missiondata import JtacInfo, MissionData

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

INFANTRY_GROUP_SIZE = 5


class FlotGenerator:
    def __init__(
        self,
        mission: Mission,
        conflict: FrontLineConflictDescription,
        game: Game,
        player_planned_combat_groups: List[CombatGroup],
        enemy_planned_combat_groups: List[CombatGroup],
        player_stance: CombatStance,
        enemy_stance: CombatStance,
        unit_map: UnitMap,
        radio_registry: RadioRegistry,
        mission_data: MissionData,
        laser_code_registry: LaserCodeRegistry,
    ) -> None:
        self.mission = mission
        self.conflict = conflict
        self.enemy_planned_combat_groups = enemy_planned_combat_groups
        self.player_planned_combat_groups = player_planned_combat_groups
        self.player_stance = player_stance
        self.enemy_stance = enemy_stance
        self.game = game
        self.unit_map = unit_map
        self.radio_registry = radio_registry
        self.mission_data = mission_data
        self.laser_code_registry = laser_code_registry

    def generate(self) -> None:
        position = FrontLineConflictDescription.frontline_position(
            self.conflict.front_line, self.game.theater
        )

        # Create player groups at random position
        player_groups = self._generate_groups(
            self.player_planned_combat_groups, is_player=True
        )

        # Create enemy groups at random position
        enemy_groups = self._generate_groups(
            self.enemy_planned_combat_groups, is_player=False
        )

        # TODO: Differentiate AirConflict and GroundConflict classes.
        if self.conflict.heading is None:
            raise RuntimeError(
                "Cannot generate ground units for non-ground conflict. Ground unit "
                "conflicts cannot have the heading `None`."
            )

        # Plan combat actions for groups
        self.plan_action_for_groups(
            self.player_stance,
            player_groups,
            enemy_groups,
            self.conflict.heading.right,
            self.conflict.blue_cp,
            self.conflict.red_cp,
        )
        self.plan_action_for_groups(
            self.enemy_stance,
            enemy_groups,
            player_groups,
            self.conflict.heading.left,
            self.conflict.red_cp,
            self.conflict.blue_cp,
        )

        # Add JTAC
        if self.game.blue.faction.has_jtac:
            code: int
            freq = self.radio_registry.alloc_uhf()
            # If the option fc3LaserCode is enabled, force all JTAC
            # laser codes to 1113 to allow lasing for Su-25 Frogfoots and A-10A Warthogs.
            # Otherwise use 1688 for the first JTAC, 1687 for the second etc.
            if self.game.settings.plugins["plugins.ctld.fc3LaserCode"]:
                code = 1113
            else:
                code = self.laser_code_registry.get_next_laser_code()

            utype = self.game.blue.faction.jtac_unit
            if utype is None:
                utype = AircraftType.named("MQ-9 Reaper")

            jtac = self.mission.flight_group(
                country=self.mission.country(self.game.blue.country_name),
                name=namegen.next_jtac_name(),
                aircraft_type=utype.dcs_unit_type,
                position=position[0],
                airport=None,
                altitude=5000,
                maintask=AFAC,
            )
            jtac.points[0].tasks.append(
                FAC(
                    callsign=len(self.mission_data.jtacs) + 1,
                    frequency=int(freq.mhz),
                    modulation=freq.modulation,
                )
            )
            jtac.points[0].tasks.append(SetInvisibleCommand(True))
            jtac.points[0].tasks.append(SetImmortalCommand(True))
            jtac.points[0].tasks.append(
                OrbitAction(5000, 300, OrbitAction.OrbitPattern.Circle)
            )
            frontline = (
                f"Frontline {self.conflict.blue_cp.name}/{self.conflict.red_cp.name}"
            )
            # Note: Will need to change if we ever add ground based JTAC.
            callsign = callsign_for_support_unit(jtac)
            self.mission_data.jtacs.append(
                JtacInfo(
                    group_name=jtac.name,
                    unit_name=jtac.units[0].name,
                    callsign=callsign,
                    region=frontline,
                    code=str(code),
                    blue=True,
                    freq=freq,
                )
            )

    def gen_infantry_group_for_group(
        self,
        group: VehicleGroup,
        is_player: bool,
        side: Country,
        forward_heading: Heading,
    ) -> None:

        infantry_position = self.conflict.find_ground_position(
            group.points[0].position.random_point_within(250, 50),
            500,
            forward_heading,
            self.conflict.theater,
        )

        faction = self.game.faction_for(is_player)

        # Disable infantry unit gen if disabled
        if not self.game.settings.perf_infantry:
            if self.game.settings.manpads:
                # 50% of armored units protected by manpad
                if random.choice([True, False]):
                    manpads = list(faction.infantry_with_class(UnitClass.MANPAD))
                    if manpads:
                        u = random.choices(
                            manpads, weights=[m.spawn_weight for m in manpads]
                        )[0]
                        self.mission.vehicle_group(
                            side,
                            namegen.next_infantry_name(side, u),
                            u.dcs_unit_type,
                            position=infantry_position,
                            group_size=1,
                            heading=forward_heading.degrees,
                            move_formation=PointAction.OffRoad,
                        )
            return

        possible_infantry_units = set(faction.infantry_with_class(UnitClass.INFANTRY))
        if self.game.settings.manpads:
            possible_infantry_units |= set(
                faction.infantry_with_class(UnitClass.MANPAD)
            )
        if not possible_infantry_units:
            return

        infantry_choices = list(possible_infantry_units)
        units = random.choices(
            infantry_choices,
            weights=[u.spawn_weight for u in infantry_choices],
            k=INFANTRY_GROUP_SIZE,
        )
        self.mission.vehicle_group(
            side,
            namegen.next_infantry_name(side, units[0]),
            units[0].dcs_unit_type,
            position=infantry_position,
            group_size=1,
            heading=forward_heading.degrees,
            move_formation=PointAction.OffRoad,
        )

        for unit in units[1:]:
            position = infantry_position.random_point_within(55, 5)
            self.mission.vehicle_group(
                side,
                namegen.next_infantry_name(side, unit),
                unit.dcs_unit_type,
                position=position,
                group_size=1,
                heading=forward_heading.degrees,
                move_formation=PointAction.OffRoad,
            )

    def _set_reform_waypoint(
        self, dcs_group: VehicleGroup, forward_heading: Heading
    ) -> None:
        """Setting a waypoint close to the spawn position allows the group to reform gracefully
        rather than spin
        """
        reform_point = dcs_group.position.point_from_heading(
            forward_heading.degrees, 50
        )
        dcs_group.add_waypoint(reform_point)

    def _plan_artillery_action(
        self,
        stance: CombatStance,
        gen_group: CombatGroup,
        dcs_group: VehicleGroup,
        forward_heading: Heading,
        target: Point,
    ) -> bool:
        """
        Handles adding the DCS tasks for artillery groups for all combat stances.
        Returns True if tasking was added, returns False if the stance was not a combat stance.
        """
        self._set_reform_waypoint(dcs_group, forward_heading)
        if stance != CombatStance.RETREAT:
            hold_task = Hold()
            hold_task.number = 1
            dcs_group.add_trigger_action(hold_task)

        # Artillery strike random start
        artillery_trigger = TriggerOnce(
            Event.NoEvent, "ArtilleryFireTask #" + str(dcs_group.id)
        )
        artillery_trigger.add_condition(TimeAfter(seconds=random.randint(1, 45) * 60))
        # TODO: Update to fire at group instead of point
        fire_task = FireAtPoint(target, gen_group.size * 10, 100)
        fire_task.number = 2 if stance != CombatStance.RETREAT else 1
        dcs_group.add_trigger_action(fire_task)
        artillery_trigger.add_action(AITaskPush(dcs_group.id, len(dcs_group.tasks)))
        self.mission.triggerrules.triggers.append(artillery_trigger)

        # Artillery will fall back when under attack
        if stance != CombatStance.RETREAT:

            # Hold position
            dcs_group.points[1].tasks.append(Hold())
            retreat = self.find_retreat_point(
                dcs_group, forward_heading, (int)(RETREAT_DISTANCE / 3)
            )
            dcs_group.add_waypoint(
                dcs_group.position.point_from_heading(forward_heading.degrees, 1),
                PointAction.OffRoad,
            )
            dcs_group.points[2].tasks.append(Hold())
            dcs_group.add_waypoint(retreat, PointAction.OffRoad)

            artillery_fallback = TriggerOnce(
                Event.NoEvent, "ArtilleryRetreat #" + str(dcs_group.id)
            )
            for i, u in enumerate(dcs_group.units):
                artillery_fallback.add_condition(UnitDamaged(u.id))
                if i < len(dcs_group.units) - 1:
                    artillery_fallback.add_condition(Or())

            hold_2 = Hold()
            hold_2.number = 3
            dcs_group.add_trigger_action(hold_2)

            retreat_task = GoToWaypoint(to_index=3)
            retreat_task.number = 4
            dcs_group.add_trigger_action(retreat_task)

            artillery_fallback.add_action(
                AITaskPush(dcs_group.id, len(dcs_group.tasks))
            )
            self.mission.triggerrules.triggers.append(artillery_fallback)

            for u in dcs_group.units:
                u.heading = (forward_heading + Heading.random(-5, 5)).degrees
            return True
        return False

    def _plan_tank_ifv_action(
        self,
        stance: CombatStance,
        enemy_groups: List[Tuple[VehicleGroup, CombatGroup]],
        dcs_group: VehicleGroup,
        forward_heading: Heading,
        to_cp: ControlPoint,
    ) -> bool:
        """
        Handles adding the DCS tasks for tank and IFV groups for all combat stances.
        Returns True if tasking was added, returns False if the stance was not a combat stance.
        """
        self._set_reform_waypoint(dcs_group, forward_heading)
        if stance == CombatStance.AGGRESSIVE:
            # Attack nearest enemy if any
            # Then move forward OR Attack enemy base if it is not too far away
            target = self.find_nearest_enemy_group(dcs_group, enemy_groups)
            if target is not None:
                rand_offset = Vector2(
                    random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK),
                    random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK),
                )
                target_point = self.conflict.theater.nearest_land_pos(
                    target.points[0].position + rand_offset
                )
                dcs_group.add_waypoint(target_point)
                dcs_group.points[2].tasks.append(AttackGroup(target.id))

            if (
                to_cp.position.distance_to_point(dcs_group.points[0].position)
                <= AGGRESIVE_MOVE_DISTANCE
            ):
                attack_point = self.conflict.theater.nearest_land_pos(
                    to_cp.position.random_point_within(500, 0)
                )
            else:
                # We use an offset heading here because DCS doesn't always
                # force vehicles to move if there's no heading change.
                offset_heading = forward_heading - Heading.from_degrees(2)
                attack_point = self.find_offensive_point(
                    dcs_group, offset_heading, AGGRESIVE_MOVE_DISTANCE
                )
            dcs_group.add_waypoint(attack_point, PointAction.OffRoad)
        elif stance == CombatStance.BREAKTHROUGH:
            # In breakthrough mode, the units will move forward
            # If the enemy base is close enough, the units will attack the base
            if (
                to_cp.position.distance_to_point(dcs_group.points[0].position)
                <= BREAKTHROUGH_OFFENSIVE_DISTANCE
            ):
                attack_point = self.conflict.theater.nearest_land_pos(
                    to_cp.position.random_point_within(500, 0)
                )
            else:
                # We use an offset heading here because DCS doesn't always
                # force vehicles to move if there's no heading change.
                offset_heading = forward_heading - Heading.from_degrees(1)
                attack_point = self.find_offensive_point(
                    dcs_group, offset_heading, BREAKTHROUGH_OFFENSIVE_DISTANCE
                )
            dcs_group.add_waypoint(attack_point, PointAction.OffRoad)
        elif stance == CombatStance.ELIMINATION:
            # In elimination mode, the units focus on destroying as much enemy groups as possible
            targets = self.find_n_nearest_enemy_groups(dcs_group, enemy_groups, 3)
            for i, target in enumerate(targets, start=1):
                rand_offset = Vector2(
                    random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK),
                    random.randint(-RANDOM_OFFSET_ATTACK, RANDOM_OFFSET_ATTACK),
                )
                target_point = self.conflict.theater.nearest_land_pos(
                    target.points[0].position + rand_offset
                )
                dcs_group.add_waypoint(target_point, PointAction.OffRoad)
                dcs_group.points[i + 1].tasks.append(AttackGroup(target.id))
            if (
                to_cp.position.distance_to_point(dcs_group.points[0].position)
                <= AGGRESIVE_MOVE_DISTANCE
            ):
                attack_point = self.conflict.theater.nearest_land_pos(
                    to_cp.position.random_point_within(500, 0)
                )
                dcs_group.add_waypoint(attack_point)

        if stance != CombatStance.RETREAT:
            self.add_morale_trigger(dcs_group, forward_heading)
            return True
        return False

    def _plan_apc_atgm_action(
        self,
        stance: CombatStance,
        dcs_group: VehicleGroup,
        forward_heading: Heading,
        to_cp: ControlPoint,
    ) -> bool:
        """
        Handles adding the DCS tasks for APC and ATGM groups for all combat stances.
        Returns True if tasking was added, returns False if the stance was not a combat stance.
        """
        self._set_reform_waypoint(dcs_group, forward_heading)
        if stance in [
            CombatStance.AGGRESSIVE,
            CombatStance.BREAKTHROUGH,
            CombatStance.ELIMINATION,
        ]:
            # APC & ATGM will never move too much forward, but will follow along any offensive
            if (
                to_cp.position.distance_to_point(dcs_group.points[0].position)
                <= AGGRESIVE_MOVE_DISTANCE
            ):
                attack_point = self.conflict.theater.nearest_land_pos(
                    to_cp.position.random_point_within(500, 0)
                )
            else:
                attack_point = self.find_offensive_point(
                    dcs_group, forward_heading, AGGRESIVE_MOVE_DISTANCE
                )
            dcs_group.add_waypoint(attack_point, PointAction.OffRoad)

        if stance != CombatStance.RETREAT:
            self.add_morale_trigger(dcs_group, forward_heading)
            return True
        return False

    def plan_action_for_groups(
        self,
        stance: CombatStance,
        ally_groups: List[Tuple[VehicleGroup, CombatGroup]],
        enemy_groups: List[Tuple[VehicleGroup, CombatGroup]],
        forward_heading: Heading,
        from_cp: ControlPoint,
        to_cp: ControlPoint,
    ) -> None:

        if not self.game.settings.perf_moving_units:
            return

        for dcs_group, group in ally_groups:
            if group.unit_type.eplrs_capable:
                dcs_group.points[0].tasks.append(EPLRS(dcs_group.id))

            if group.role == CombatGroupRole.ARTILLERY:
                if self.game.settings.perf_artillery:
                    target = self.get_artillery_target_in_range(
                        dcs_group, group, enemy_groups
                    )
                    if target is not None:
                        self._plan_artillery_action(
                            stance, group, dcs_group, forward_heading, target
                        )

            elif group.role in [CombatGroupRole.TANK, CombatGroupRole.IFV]:
                self._plan_tank_ifv_action(
                    stance, enemy_groups, dcs_group, forward_heading, to_cp
                )

            elif group.role in [CombatGroupRole.APC, CombatGroupRole.ATGM]:
                self._plan_apc_atgm_action(stance, dcs_group, forward_heading, to_cp)

            if stance == CombatStance.RETREAT:
                # In retreat mode, the units will fall back
                # If the ally base is close enough, the units will even regroup there
                if (
                    from_cp.position.distance_to_point(dcs_group.points[0].position)
                    <= RETREAT_DISTANCE
                ):
                    retreat_point = from_cp.position.random_point_within(500, 250)
                else:
                    retreat_point = self.find_retreat_point(dcs_group, forward_heading)
                reposition_point = retreat_point.point_from_heading(
                    forward_heading.degrees, 10
                )  # Another point to make the unit face the enemy
                dcs_group.add_waypoint(retreat_point, PointAction.OffRoad)
                dcs_group.add_waypoint(reposition_point, PointAction.OffRoad)

    def add_morale_trigger(
        self, dcs_group: VehicleGroup, forward_heading: Heading
    ) -> None:
        """
        This add a trigger to manage units fleeing whenever their group is hit hard, or being engaged by CAS
        """

        if len(dcs_group.units) == 1:
            return

        # Units should hold position on last waypoint
        dcs_group.points[len(dcs_group.points) - 1].tasks.append(Hold())

        # Force unit heading
        for unit in dcs_group.units:
            unit.heading = forward_heading.degrees
        dcs_group.manualHeading = True

        # We add a new retreat waypoint
        dcs_group.add_waypoint(
            self.find_retreat_point(
                dcs_group, forward_heading, (int)(RETREAT_DISTANCE / 8)
            ),
            PointAction.OffRoad,
        )

        # Fallback task
        task = ControlledTask(GoToWaypoint(to_index=len(dcs_group.points)))
        task.enabled = False
        dcs_group.add_trigger_action(Hold())
        dcs_group.add_trigger_action(task)

        # Create trigger
        fallback = TriggerOnce(Event.NoEvent, "Morale manager #" + str(dcs_group.id))

        # Usually more than 50% casualties = RETREAT
        fallback.add_condition(GroupLifeLess(dcs_group.id, random.randint(51, 76)))

        # Do retreat to the configured retreat waypoint
        fallback.add_action(AITaskPush(dcs_group.id, len(dcs_group.tasks)))

        self.mission.triggerrules.triggers.append(fallback)

    def find_retreat_point(
        self,
        dcs_group: VehicleGroup,
        frontline_heading: Heading,
        distance: int = RETREAT_DISTANCE,
    ) -> Point:
        """
        Find a point to retreat to
        :param dcs_group: DCS mission group we are searching a retreat point for
        :param frontline_heading: Heading of the frontline
        :return: dcs.mapping.Point object with the desired position
        """
        desired_point = dcs_group.points[0].position.point_from_heading(
            frontline_heading.opposite.degrees, distance
        )
        if self.conflict.theater.is_on_land(desired_point):
            return desired_point
        return self.conflict.theater.nearest_land_pos(desired_point)

    def find_offensive_point(
        self, dcs_group: VehicleGroup, frontline_heading: Heading, distance: int
    ) -> Point:
        """
        Find a point to attack
        :param dcs_group:  DCS mission group we are searching an attack point for
        :param frontline_heading: Heading of the frontline
        :param distance: Distance of the offensive (how far unit should move)
        :return: dcs.mapping.Point object with the desired position
        """
        desired_point = dcs_group.points[0].position.point_from_heading(
            frontline_heading.degrees, distance
        )
        if self.conflict.theater.is_on_land(desired_point):
            return desired_point
        return self.conflict.theater.nearest_land_pos(desired_point)

    @staticmethod
    def find_n_nearest_enemy_groups(
        player_group: VehicleGroup,
        enemy_groups: List[Tuple[VehicleGroup, CombatGroup]],
        n: int,
    ) -> List[VehicleGroup]:
        """
        Return the nearest enemy group for the player group
        @param group Group for which we should find the nearest ennemies
        @param enemy_groups Potential enemy groups
        @param n number of nearby groups to take
        """
        targets = []  # type: List[VehicleGroup]
        sorted_list = sorted(
            enemy_groups,
            key=lambda group: player_group.points[0].position.distance_to_point(
                group[0].points[0].position
            ),
        )
        for i in range(n):
            # TODO: Is this supposed to return no groups if enemy_groups is less than n?
            if len(sorted_list) <= i:
                break
            else:
                targets.append(sorted_list[i][0])
        return targets

    @staticmethod
    def find_nearest_enemy_group(
        player_group: VehicleGroup, enemy_groups: List[Tuple[VehicleGroup, CombatGroup]]
    ) -> Optional[VehicleGroup]:
        """
        Search the enemy groups for a potential target suitable to armored assault
        @param group Group for which we should find the nearest ennemy
        @param enemy_groups Potential enemy groups
        """
        min_distance = math.inf
        target = None
        for dcs_group, _ in enemy_groups:
            dist = player_group.points[0].position.distance_to_point(
                dcs_group.points[0].position
            )
            if dist < min_distance:
                min_distance = dist
                target = dcs_group
        return target

    @staticmethod
    def get_artillery_target_in_range(
        dcs_group: VehicleGroup,
        group: CombatGroup,
        enemy_groups: List[Tuple[VehicleGroup, CombatGroup]],
    ) -> Optional[Point]:
        """
        Search the enemy groups for a potential target suitable to an artillery unit
        """
        # TODO: Update to return a list of groups instead of a single point
        rng = getattr(group.unit_type.dcs_unit_type, "threat_range", 0)
        if not enemy_groups:
            return None
        for _ in range(10):
            potential_target = random.choice(enemy_groups)[0]
            distance_to_target = dcs_group.points[0].position.distance_to_point(
                potential_target.points[0].position
            )
            if distance_to_target < rng:
                return potential_target.points[0].position
        return None

    @staticmethod
    def get_artilery_group_distance_from_frontline(group: CombatGroup) -> int:
        """
        For artilery group, decide the distance from frontline with the range of the unit
        """
        rg = group.unit_type.dcs_unit_type.threat_range - 7500
        if rg > DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY][1]:
            rg = random.randint(
                DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY][0],
                DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY][1],
            )
        elif rg < DISTANCE_FROM_FRONTLINE[CombatGroupRole.ARTILLERY][1]:
            rg = random.randint(
                DISTANCE_FROM_FRONTLINE[CombatGroupRole.TANK][0],
                DISTANCE_FROM_FRONTLINE[CombatGroupRole.TANK][1],
            )
        return rg

    def get_valid_position_for_group(
        self, distance_from_frontline: int, spawn_heading: Heading
    ) -> Point:
        assert self.conflict.heading is not None
        assert self.conflict.size is not None
        shifted = self.conflict.position.point_from_heading(
            self.conflict.heading.degrees,
            random.randint(0, self.conflict.size),
        )
        desired_point = shifted.point_from_heading(
            spawn_heading.degrees, distance_from_frontline
        )
        return FrontLineConflictDescription.find_ground_position(
            desired_point,
            self.conflict.size,
            self.conflict.heading,
            self.conflict.theater,
        )

    def _generate_groups(
        self, groups: list[CombatGroup], is_player: bool
    ) -> List[Tuple[VehicleGroup, CombatGroup]]:
        """Finds valid positions for planned groups and generates a pydcs group for them"""
        positioned_groups = []
        assert self.conflict.heading is not None
        spawn_heading = (
            self.conflict.heading.left if is_player else self.conflict.heading.right
        )
        country = self.game.coalition_for(is_player).country_name
        for group in groups:
            if group.role == CombatGroupRole.ARTILLERY:
                distance_from_frontline = (
                    self.get_artilery_group_distance_from_frontline(group)
                )
            else:
                distance_from_frontline = random.randint(
                    DISTANCE_FROM_FRONTLINE[group.role][0],
                    DISTANCE_FROM_FRONTLINE[group.role][1],
                )

            final_position = self.get_valid_position_for_group(
                distance_from_frontline, spawn_heading
            )

            g = self._generate_group(
                is_player,
                self.mission.country(country),
                group.unit_type,
                group.size,
                final_position,
                heading=spawn_heading.opposite,
            )
            if is_player:
                g.set_skill(Skill(self.game.settings.player_skill))
            else:
                g.set_skill(Skill(self.game.settings.enemy_vehicle_skill))
            positioned_groups.append((g, group))

            if group.role in [CombatGroupRole.APC, CombatGroupRole.IFV]:
                self.gen_infantry_group_for_group(
                    g,
                    is_player,
                    self.mission.country(country),
                    spawn_heading.opposite,
                )

        return positioned_groups

    def _generate_group(
        self,
        player: bool,
        side: Country,
        unit_type: GroundUnitType,
        count: int,
        at: Point,
        heading: Heading,
    ) -> VehicleGroup:
        cp = self.conflict.front_line.control_point_friendly_to(player)
        group = self.mission.vehicle_group(
            side,
            namegen.next_unit_name(side, unit_type),
            unit_type.dcs_unit_type,
            position=at,
            group_size=count,
            heading=heading.degrees,
        )

        self.unit_map.add_front_line_units(group, cp, unit_type)

        for c in range(count):
            vehicle: Vehicle = group.units[c]
            vehicle.player_can_drive = True

        return group
