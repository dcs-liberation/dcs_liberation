from __future__ import annotations

import dataclasses
import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Union, Optional

from game.commander.garrisons import Garrisons
from game.commander.objectivefinder import ObjectiveFinder
from game.data.doctrine import Doctrine
from game.htn import WorldState
from game.settings import AutoAtoBehavior
from game.theater import ControlPoint, FrontLine, MissionTarget
from game.theater.theatergroundobject import (
    TheaterGroundObject,
    NavalGroundObject,
    IadsGroundObject,
    VehicleGroupGroundObject,
)
from game.threatzones import ThreatZones
from game.transfers import Convoy, CargoShip
from gen.ground_forces.combat_stance import CombatStance

if TYPE_CHECKING:
    from game import Game


@dataclass
class TheaterState(WorldState["TheaterState"]):
    player: bool
    stance_automation_enabled: bool
    ato_automation_enabled: bool
    vulnerable_control_points: list[ControlPoint]
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
    strike_targets: list[TheaterGroundObject[Any]]
    enemy_barcaps: list[ControlPoint]
    threat_zones: ThreatZones
    opposing_doctrine: Doctrine

    def _rebuild_threat_zones(self) -> None:
        """Recreates the theater's threat zones based on the current planned state."""
        self.threat_zones = ThreatZones.for_threats(
            self.opposing_doctrine,
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

    def clone(self) -> TheaterState:
        # Do not use copy.deepcopy. Copying every TGO, control point, etc is absurdly
        # expensive.
        return TheaterState(
            player=self.player,
            stance_automation_enabled=self.stance_automation_enabled,
            ato_automation_enabled=self.ato_automation_enabled,
            vulnerable_control_points=list(self.vulnerable_control_points),
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
            opposing_doctrine=self.opposing_doctrine,
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
    def from_game(cls, game: Game, player: bool) -> TheaterState:
        finder = ObjectiveFinder(game, player)
        auto_stance = game.settings.automate_front_line_stance
        auto_ato = game.settings.auto_ato_behavior is not AutoAtoBehavior.Disabled
        ordered_capturable_points = finder.prioritized_unisolated_points()
        return TheaterState(
            player=player,
            stance_automation_enabled=auto_stance,
            ato_automation_enabled=auto_ato,
            vulnerable_control_points=list(finder.vulnerable_control_points()),
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
            opposing_doctrine=game.faction_for(not player).doctrine,
        )
