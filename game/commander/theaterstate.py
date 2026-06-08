from __future__ import annotations

import dataclasses
import itertools
import math
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Union

from game.commander.battlepositions import BattlePositions
from game.commander.objectivefinder import ObjectiveFinder
from game.db import GameDb
from game.ground_forces.combat_stance import CombatStance
from game.htn import WorldState
from game.profiling import MultiEventTracer
from game.settings import Settings
from game.theater import ConflictTheater, ControlPoint, FrontLine, MissionTarget
from game.theater.theatergroundobject import (
    BuildingGroundObject,
    IadsGroundObject,
    NavalGroundObject,
    TheaterGroundObject,
    VehicleGroupGroundObject,
)
from game.threatzones import ThreatZones
from game.ato.flighttype import FlightType

if TYPE_CHECKING:
    from game import Game
    from game.coalition import Coalition
    from game.transfers import Convoy, CargoShip


@dataclass(frozen=True)
class PersistentContext:
    game_db: GameDb
    coalition: Coalition
    theater: ConflictTheater
    turn: int
    now: datetime
    settings: Settings
    tracer: MultiEventTracer


@dataclass
class TheaterState(WorldState["TheaterState"]):
    context: PersistentContext
    barcaps_needed: dict[ControlPoint, int]
    active_front_lines: list[FrontLine]
    front_line_stances: dict[FrontLine, Optional[CombatStance]]
    vulnerable_front_lines: list[FrontLine]
    aewc_targets: list[MissionTarget]
    refueling_targets: list[MissionTarget]
    enemy_air_defenses: list[IadsGroundObject]
    threatening_air_defenses: list[Union[IadsGroundObject, NavalGroundObject]]
    detecting_air_defenses: list[Union[IadsGroundObject, NavalGroundObject]]
    enemy_convoys: list[Convoy]
    enemy_shipping: list[CargoShip]
    enemy_ships: list[NavalGroundObject]
    enemy_battle_positions: dict[ControlPoint, BattlePositions]
    oca_targets: list[ControlPoint]
    enemy_carriers: list[ControlPoint]
    strike_targets: list[TheaterGroundObject]
    enemy_barcaps: list[ControlPoint]
    threat_zones: ThreatZones

    def _rebuild_threat_zones(self) -> None:
        """Recreates the theater's threat zones based on the current planned state."""
        self.threat_zones = ThreatZones.for_threats(
            self.context.theater,
            self.context.coalition.opponent.doctrine,
            barcap_locations=self.enemy_barcaps,
            air_defenses=itertools.chain(self.enemy_air_defenses, self.enemy_ships),
        )

    def eliminate_air_defense(self, target: IadsGroundObject) -> None:
        if target in self.threatening_air_defenses:
            self.threatening_air_defenses.remove(target)
        if target in self.detecting_air_defenses:
            self.detecting_air_defenses.remove(target)
        if target in self.enemy_air_defenses:
            self.enemy_air_defenses.remove(target)
        self._rebuild_threat_zones()

    def eliminate_ship(self, target: NavalGroundObject) -> None:
        if target in self.threatening_air_defenses:
            self.threatening_air_defenses.remove(target)
        if target in self.detecting_air_defenses:
            self.detecting_air_defenses.remove(target)
        if target in self.enemy_ships:
            self.enemy_ships.remove(target)
        self._rebuild_threat_zones()

    def has_battle_position(self, target: VehicleGroupGroundObject) -> bool:
        if target.control_point not in self.enemy_battle_positions:
            return False
        return target in self.enemy_battle_positions[target.control_point]

    def eliminate_battle_position(self, target: VehicleGroupGroundObject) -> None:
        if target.control_point in self.enemy_battle_positions:
            self.enemy_battle_positions[target.control_point].eliminate(target)

    def ammo_dumps_at(
        self, control_point: ControlPoint
    ) -> Iterator[BuildingGroundObject]:
        for target in self.strike_targets:
            if target.control_point != control_point:
                continue
            if target.is_ammo_depot:
                assert isinstance(target, BuildingGroundObject)
                yield target

    def clone(self) -> TheaterState:
        # Do not use copy.deepcopy. Copying every TGO, control point, etc is absurdly
        # expensive.
        return TheaterState(
            context=self.context,
            barcaps_needed=dict(self.barcaps_needed),
            active_front_lines=list(self.active_front_lines),
            front_line_stances=dict(self.front_line_stances),
            vulnerable_front_lines=list(self.vulnerable_front_lines),
            aewc_targets=list(self.aewc_targets),
            refueling_targets=list(self.refueling_targets),
            enemy_air_defenses=list(self.enemy_air_defenses),
            enemy_convoys=list(self.enemy_convoys),
            enemy_shipping=list(self.enemy_shipping),
            enemy_ships=list(self.enemy_ships),
            enemy_battle_positions={
                cp: dataclasses.replace(g)
                for cp, g in self.enemy_battle_positions.items()
            },
            oca_targets=list(self.oca_targets),
            enemy_carriers=list(self.enemy_carriers),
            strike_targets=list(self.strike_targets),
            enemy_barcaps=list(self.enemy_barcaps),
            threat_zones=self.threat_zones,
            # Persistent properties are not copied. These are a way for failed subtasks
            # to communicate requirements to other tasks. For example, the task to
            # attack enemy battle_positions might fail because the target area has IADS
            # protection. In that case, the preconditions of PlanBai would fail, but
            # would add the IADS that prevented it from being planned to the list of
            # IADS threats so that DegradeIads will consider it a threat later.
            threatening_air_defenses=self.threatening_air_defenses,
            detecting_air_defenses=self.detecting_air_defenses,
        )

    @classmethod
    def from_game(
        cls, game: Game, player: bool, now: datetime, tracer: MultiEventTracer
    ) -> TheaterState:
        coalition = game.coalition_for(player)
        finder = ObjectiveFinder(game, player)
        ordered_capturable_points = finder.prioritized_unisolated_points()

        context = PersistentContext(
            game.db,
            coalition,
            game.theater,
            game.turn,
            now,
            game.settings,
            tracer,
        )

        refueling_targets: list[MissionTarget] = []
        theater_refuling_point = finder.preferred_theater_refueling_control_point()
        if theater_refuling_point is not None:
            refueling_targets.append(theater_refuling_point)

        theater_state = TheaterState(
            context=context,
            barcaps_needed={
                cp: cls._barcap_rounds(game, player, now, cp)
                for cp in finder.vulnerable_control_points()
            },
            active_front_lines=list(finder.front_lines()),
            front_line_stances={f: None for f in finder.front_lines()},
            vulnerable_front_lines=list(finder.front_lines()),
            aewc_targets=[finder.farthest_friendly_control_point()],
            refueling_targets=refueling_targets,
            enemy_air_defenses=list(finder.enemy_air_defenses()),
            threatening_air_defenses=[],
            detecting_air_defenses=[],
            enemy_convoys=list(finder.convoys()),
            enemy_shipping=list(finder.cargo_ships()),
            enemy_ships=list(finder.enemy_ships()),
            enemy_battle_positions={
                cp: BattlePositions.for_control_point(cp)
                for cp in ordered_capturable_points
            },
            oca_targets=list(finder.oca_targets(min_aircraft=20)),
            enemy_carriers=list(finder.enemy_carriers()),
            strike_targets=list(finder.strike_targets()),
            enemy_barcaps=list(game.theater.control_points_for(not player)),
            threat_zones=game.threat_zone_for(not player),
        )

        # Look through packages already planned in the ATO and eliminate from the
        # list of targets.
        for package in coalition.ato.packages:
            if isinstance(package.target, NavalGroundObject):
                theater_state.eliminate_ship(package.target)
            if package.primary_task == FlightType.BAI and isinstance(
                package.target, VehicleGroupGroundObject
            ):
                theater_state.eliminate_battle_position(package.target)
            if isinstance(package.target, IadsGroundObject):
                theater_state.eliminate_air_defense(package.target)
            if (
                package.primary_task == FlightType.STRIKE
                and isinstance(package.target, TheaterGroundObject)
                and package.target in theater_state.strike_targets
            ):
                theater_state.strike_targets.remove(package.target)
            if package.primary_task == FlightType.AEWC:
                # If a planned AEWC mission covers the target beyond the planned mission duration, it can safely be removed
                if (
                    package.time_over_target + coalition.doctrine.aewc.duration
                    > now + game.settings.desired_player_mission_duration
                ) and package.target in theater_state.aewc_targets:
                    theater_state.aewc_targets.remove(package.target)
            if (
                package.primary_task
                in (
                    FlightType.OCA_AIRCRAFT,
                    FlightType.OCA_RUNWAY,
                )
                and isinstance(package.target, ControlPoint)
                and package.target in theater_state.oca_targets
            ):
                theater_state.oca_targets.remove(package.target)
        return theater_state

    @classmethod
    def _barcap_rounds(
        cls, game: Game, player: bool, now: datetime, control_point: ControlPoint
    ) -> int:
        """Calculate number of additional rounds of CAP required to cover mission duration."""
        coalition = game.coalition_for(player)

        # Look through ATO for any existing planned CAP missions and calculate last planned CAP end
        planned_cap_coverage_end_time = now
        for package in coalition.ato.packages:
            if package.target == control_point:
                cap_end_time = (
                    package.time_over_target + coalition.doctrine.cap.duration
                )
                if cap_end_time > planned_cap_coverage_end_time:
                    planned_cap_coverage_end_time = cap_end_time
        # When mission is expected to finish
        mission_end_time = now + game.settings.desired_player_mission_duration
        return math.ceil(
            (mission_end_time - planned_cap_coverage_end_time).total_seconds()
            / coalition.doctrine.cap.duration.total_seconds()
        )
