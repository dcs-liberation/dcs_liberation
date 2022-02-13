from __future__ import annotations

from pydantic import Field
from pydantic.main import BaseModel

from game import Game
from game.ato import Flight
from game.flightplan import JoinZoneGeometry
from .config import ENABLE_EXPENSIVE_DEBUG_TOOLS
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class JoinZonesJs(BaseModel):
    home_bubble: LeafletPoly = Field(alias="homeBubble")
    target_bubble: LeafletPoly = Field(alias="targetBubble")
    ip_bubble: LeafletPoly = Field(alias="ipBubble")
    excluded_zones: list[LeafletPoly] = Field(alias="excludedZones")
    permissible_zones: list[LeafletPoly] = Field(alias="permissibleZones")
    preferred_lines: list[LeafletPoly] = Field(alias="preferredLines")

    @classmethod
    def empty(cls) -> JoinZonesJs:
        return JoinZonesJs(
            homeBubble=[],
            targetBubble=[],
            ipBubble=[],
            excludedZones=[],
            permissibleZones=[],
            preferredLines=[],
        )

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> JoinZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return JoinZonesJs.empty()
        target = flight.package.target
        home = flight.departure
        if flight.package.waypoints is None:
            return JoinZonesJs.empty()
        ip = flight.package.waypoints.ingress
        geometry = JoinZoneGeometry(target.position, home.position, ip, game.blue)
        return JoinZonesJs(
            homeBubble=ShapelyUtil.poly_to_leaflet(geometry.home_bubble, game.theater),
            targetBubble=ShapelyUtil.poly_to_leaflet(
                geometry.target_bubble, game.theater
            ),
            ipBubble=ShapelyUtil.poly_to_leaflet(geometry.ip_bubble, game.theater),
            excludedZones=ShapelyUtil.polys_to_leaflet(
                geometry.excluded_zones, game.theater
            ),
            permissibleZones=ShapelyUtil.polys_to_leaflet(
                geometry.permissible_zones, game.theater
            ),
            preferredLines=ShapelyUtil.lines_to_leaflet(
                geometry.preferred_lines, game.theater
            ),
        )
