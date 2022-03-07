from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from game.server.controlpoints.models import ControlPointJs
from game.server.flights.models import FlightJs
from game.server.frontlines.models import FrontLineJs
from game.server.leaflet import LeafletPoint
from game.server.mapzones.models import ThreatZoneContainerJs
from game.server.navmesh.models import NavMeshesJs
from game.server.supplyroutes.models import SupplyRouteJs
from game.server.tgos.models import TgoJs

if TYPE_CHECKING:
    from game import Game


class GameJs(BaseModel):
    control_points: list[ControlPointJs]
    tgos: list[TgoJs]
    supply_routes: list[SupplyRouteJs]
    front_lines: list[FrontLineJs]
    flights: list[FlightJs]
    threat_zones: ThreatZoneContainerJs
    navmeshes: NavMeshesJs
    map_center: LeafletPoint | None

    class Config:
        title = "Game"

    @staticmethod
    def from_game(game: Game) -> GameJs:
        return GameJs(
            control_points=ControlPointJs.all_in_game(game),
            tgos=TgoJs.all_in_game(game),
            supply_routes=SupplyRouteJs.all_in_game(game),
            front_lines=FrontLineJs.all_in_game(game),
            flights=FlightJs.all_in_game(game, with_waypoints=True),
            threat_zones=ThreatZoneContainerJs.for_game(game),
            navmeshes=NavMeshesJs.from_game(game),
            map_center=game.theater.terrain.map_view_default.position.latlng(),
        )
