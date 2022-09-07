from __future__ import annotations

from pydantic import BaseModel, Field

from game import Game
from game.ato import Flight
from game.flightplan import HoldZoneGeometry, IpZoneGeometry, JoinZoneGeometry
from ..leaflet import LeafletLine, LeafletPoly, ShapelyUtil


class HoldZonesJs(BaseModel):
    home_bubble: LeafletPoly = Field(alias="homeBubble")
    target_bubble: LeafletPoly = Field(alias="targetBubble")
    join_bubble: LeafletPoly = Field(alias="joinBubble")
    excluded_zones: list[LeafletPoly] = Field(alias="excludedZones")
    permissible_zones: list[LeafletPoly] = Field(alias="permissibleZones")
    preferred_lines: list[LeafletLine] = Field(alias="preferredLines")

    class Config:
        title = "HoldZones"

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


class IpZonesJs(BaseModel):
    home_bubble: LeafletPoly = Field(alias="homeBubble")
    ipBubble: LeafletPoly = Field(alias="ipBubble")
    permissibleZone: LeafletPoly = Field(alias="permissibleZone")
    safeZones: list[LeafletPoly] = Field(alias="safeZones")

    class Config:
        title = "IpZones"

    @classmethod
    def empty(cls) -> IpZonesJs:
        return IpZonesJs(homeBubble=[], ipBubble=[], permissibleZone=[], safeZones=[])

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> IpZonesJs:
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


class JoinZonesJs(BaseModel):
    home_bubble: LeafletPoly = Field(alias="homeBubble")
    target_bubble: LeafletPoly = Field(alias="targetBubble")
    ip_bubble: LeafletPoly = Field(alias="ipBubble")
    excluded_zones: list[LeafletPoly] = Field(alias="excludedZones")
    permissible_zones: list[LeafletPoly] = Field(alias="permissibleZones")
    preferred_lines: list[LeafletLine] = Field(alias="preferredLines")

    class Config:
        title = "JoinZones"

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
