from __future__ import annotations

from pydantic import BaseModel, Field

from game import Game
from game.ato import Flight
from game.flightplan import HoldZoneGeometry
from .config import ENABLE_EXPENSIVE_DEBUG_TOOLS
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class HoldZonesJs(BaseModel):
    home_bubble: LeafletPoly = Field(alias="homeBubble")
    target_bubble: LeafletPoly = Field(alias="targetBubble")
    join_bubble: LeafletPoly = Field(alias="joinBubble")
    excluded_zones: list[LeafletPoly] = Field(alias="excludedZones")
    permissible_zones: list[LeafletPoly] = Field(alias="permissibleZones")
    preferred_lines: list[LeafletPoly] = Field(alias="preferredLines")

    @classmethod
    def empty(cls) -> HoldZonesJs:
        return HoldZonesJs(
            homeBubble=[],
            targetBubble=[],
            joinBubble=[],
            excludedZones=[],
            permissibleZones=[],
            preferredLines=[],
        )

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> HoldZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return HoldZonesJs.empty()
        target = flight.package.target
        home = flight.departure
        if flight.package.waypoints is None:
            return HoldZonesJs.empty()
        ip = flight.package.waypoints.ingress
        join = flight.package.waypoints.join
        geometry = HoldZoneGeometry(
            target.position, home.position, ip, join, game.blue, game.theater
        )
        return HoldZonesJs(
            homeBubble=ShapelyUtil.poly_to_leaflet(geometry.home_bubble, game.theater),
            targetBubble=ShapelyUtil.poly_to_leaflet(
                geometry.target_bubble, game.theater
            ),
            joinBubble=ShapelyUtil.poly_to_leaflet(geometry.join_bubble, game.theater),
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
