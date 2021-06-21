from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from game.commander.objectivefinder import ObjectiveFinder
from game.htn import WorldState
from game.theater import ControlPoint, FrontLine, MissionTarget
from game.theater.theatergroundobject import (
    TheaterGroundObject,
    VehicleGroupGroundObject,
    NavalGroundObject,
    IadsGroundObject,
)
from game.transfers import Convoy, CargoShip

if TYPE_CHECKING:
    from game import Game


@dataclass
class TheaterState(WorldState["TheaterState"]):
    vulnerable_control_points: list[ControlPoint]
    vulnerable_front_lines: list[FrontLine]
    aewc_targets: list[MissionTarget]
    refueling_targets: list[MissionTarget]
    threatening_air_defenses: list[IadsGroundObject]
    enemy_convoys: list[Convoy]
    enemy_shipping: list[CargoShip]
    threatening_ships: list[NavalGroundObject]
    enemy_garrisons: list[VehicleGroupGroundObject]
    oca_targets: list[ControlPoint]
    strike_targets: list[TheaterGroundObject[Any]]

    def clone(self) -> TheaterState:
        # Do not use copy.deepcopy. Copying every TGO, control point, etc is absurdly
        # expensive.
        return TheaterState(
            vulnerable_control_points=list(self.vulnerable_control_points),
            vulnerable_front_lines=list(self.vulnerable_front_lines),
            aewc_targets=list(self.aewc_targets),
            refueling_targets=list(self.refueling_targets),
            threatening_air_defenses=list(self.threatening_air_defenses),
            enemy_convoys=list(self.enemy_convoys),
            enemy_shipping=list(self.enemy_shipping),
            threatening_ships=list(self.threatening_ships),
            enemy_garrisons=list(self.enemy_garrisons),
            oca_targets=list(self.oca_targets),
            strike_targets=list(self.strike_targets),
        )

    @classmethod
    def from_game(cls, game: Game, player: bool) -> TheaterState:
        finder = ObjectiveFinder(game, player)
        return TheaterState(
            vulnerable_control_points=list(finder.vulnerable_control_points()),
            vulnerable_front_lines=list(finder.front_lines()),
            aewc_targets=[finder.farthest_friendly_control_point()],
            refueling_targets=[finder.closest_friendly_control_point()],
            threatening_air_defenses=list(finder.threatening_air_defenses()),
            enemy_convoys=list(finder.convoys()),
            enemy_shipping=list(finder.cargo_ships()),
            threatening_ships=list(finder.threatening_ships()),
            enemy_garrisons=list(finder.threatening_vehicle_groups()),
            oca_targets=list(finder.oca_targets(min_aircraft=20)),
            strike_targets=list(finder.strike_targets()),
        )
