from __future__ import annotations

from pydantic import BaseModel, Field

from game import Game
from game.ato import Flight
from game.flightplan import IpZoneGeometry
from .config import ENABLE_EXPENSIVE_DEBUG_TOOLS
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class IpZonesJs(BaseModel):
    home_bubble: LeafletPoly = Field(alias="homeBubble")
    ipBubble: LeafletPoly = Field(alias="ipBubble")
    permissibleZone: LeafletPoly = Field(alias="permissibleZone")
    safeZones: list[LeafletPoly] = Field(alias="safeZones")

    @classmethod
    def empty(cls) -> IpZonesJs:
        return IpZonesJs(homeBubble=[], ipBubble=[], permissibleZone=[], safeZones=[])

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> IpZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return IpZonesJs.empty()
        target = flight.package.target
        home = flight.departure
        geometry = IpZoneGeometry(target.position, home.position, game.blue)
        return IpZonesJs(
            homeBubble=ShapelyUtil.poly_to_leaflet(geometry.home_bubble, game.theater),
            ipBubble=ShapelyUtil.poly_to_leaflet(geometry.ip_bubble, game.theater),
            permissibleZone=ShapelyUtil.poly_to_leaflet(
                geometry.permissible_zone, game.theater
            ),
            safeZones=ShapelyUtil.polys_to_leaflet(geometry.safe_zones, game.theater),
        )
