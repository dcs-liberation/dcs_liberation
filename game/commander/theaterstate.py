from __future__ import annotations

import dataclasses
import itertools
import math
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Optional, TYPE_CHECKING, Union

from game.commander.garrisons import Garrisons
from game.commander.objectivefinder import ObjectiveFinder
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
from gen.ground_forces.combat_stance import CombatStance

if TYPE_CHECKING:
    from game import Game
    from game.coalition import Coalition
    from game.transfers import Convoy, CargoShip


@dataclass(frozen=True)
class PersistentContext:
    coalition: Coalition
    theater: ConflictTheater
    turn: int
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
    enemy_garrisons: dict[ControlPoint, Garrisons]
    oca_targets: list[ControlPoint]
    strike_targets: list[TheaterGroundObject]
    enemy_barcaps: list[ControlPoint]
    threat_zones: ThreatZones

    def _rebuild_threat_zones(self) -> None:
        """Recreates the theater's threat zones based on the current planned state."""
        self.threat_zones = ThreatZones.for_threats(
            self.context.coalition.opponent.doctrine,
            barcap_locations=self.enemy_barcaps,
            air_defenses=itertools.chain(self.enemy_air_defenses, self.enemy_ships),
        )

    def eliminate_air_defense(self, target: IadsGroundObject) -> None:
        if target in self.threatening_air_defenses:
            self.threatening_air_defenses.remove(target)
        if target in self.detecting_air_defenses:
            self.detecting_air_defenses.remove(target)
        self.enemy_air_defenses.remove(target)
        self._rebuild_threat_zones()

    def eliminate_ship(self, target: NavalGroundObject) -> None:
        if target in self.threatening_air_defenses:
            self.threatening_air_defenses.remove(target)
        if target in self.detecting_air_defenses:
            self.detecting_air_defenses.remove(target)
        self.enemy_ships.remove(target)
        self._rebuild_threat_zones()

    def has_garrison(self, target: VehicleGroupGroundObject) -> bool:
        return target in self.enemy_garrisons[target.control_point]

    def eliminate_garrison(self, target: VehicleGroupGroundObject) -> None:
        self.enemy_garrisons[target.control_point].eliminate(target)

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
            enemy_garrisons={
                cp: dataclasses.replace(g) for cp, g in self.enemy_garrisons.items()
            },
            oca_targets=list(self.oca_targets),
            strike_targets=list(self.strike_targets),
            enemy_barcaps=list(self.enemy_barcaps),
            threat_zones=self.threat_zones,
            # Persistent properties are not copied. These are a way for failed subtasks
            # to communicate requirements to other tasks. For example, the task to
            # attack enemy garrisons might fail because the target area has IADS
            # protection. In that case, the preconditions of PlanBai would fail, but
            # would add the IADS that prevented it from being planned to the list of
            # IADS threats so that DegradeIads will consider it a threat later.
            threatening_air_defenses=self.threatening_air_defenses,
            detecting_air_defenses=self.detecting_air_defenses,
        )

    @classmethod
    def from_game(
        cls, game: Game, player: bool, tracer: MultiEventTracer
    ) -> TheaterState:
        coalition = game.coalition_for(player)
        finder = ObjectiveFinder(game, player)
        ordered_capturable_points = finder.prioritized_unisolated_points()

        context = PersistentContext(
            coalition, game.theater, game.turn, game.settings, tracer
        )

        # Plan enough rounds of CAP that the target has coverage over the expected
        # mission duration.
        mission_duration = game.settings.desired_player_mission_duration.total_seconds()
        barcap_duration = coalition.doctrine.cap_duration.total_seconds()
        barcap_rounds = math.ceil(mission_duration / barcap_duration)

        return TheaterState(
            context=context,
            barcaps_needed={
                cp: barcap_rounds for cp in finder.vulnerable_control_points()
            },
            active_front_lines=list(finder.front_lines()),
            front_line_stances={f: None for f in finder.front_lines()},
            vulnerable_front_lines=list(finder.front_lines()),
            aewc_targets=[finder.farthest_friendly_control_point()],
            refueling_targets=[finder.closest_friendly_control_point()],
            enemy_air_defenses=list(finder.enemy_air_defenses()),
            threatening_air_defenses=[],
            detecting_air_defenses=[],
            enemy_convoys=list(finder.convoys()),
            enemy_shipping=list(finder.cargo_ships()),
            enemy_ships=list(finder.enemy_ships()),
            enemy_garrisons={
                cp: Garrisons.for_control_point(cp) for cp in ordered_capturable_points
            },
            oca_targets=list(finder.oca_targets(min_aircraft=20)),
            strike_targets=list(finder.strike_targets()),
            enemy_barcaps=list(game.theater.control_points_for(not player)),
            threat_zones=game.threat_zone_for(not player),
        )
