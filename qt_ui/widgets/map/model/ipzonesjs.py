from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from game import Game
from game.ato import Flight
from game.flightplan import IpZoneGeometry
from .config import ENABLE_EXPENSIVE_DEBUG_TOOLS
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class IpZonesJs(QObject):
    homeBubbleChanged = Signal()
    ipBubbleChanged = Signal()
    permissibleZoneChanged = Signal()
    safeZonesChanged = Signal()

    def __init__(
        self,
        home_bubble: LeafletPoly,
        ip_bubble: LeafletPoly,
        permissible_zone: LeafletPoly,
        safe_zones: list[LeafletPoly],
    ) -> None:
        super().__init__()
        self._home_bubble = home_bubble
        self._ip_bubble = ip_bubble
        self._permissible_zone = permissible_zone
        self._safe_zones = safe_zones

    @Property(list, notify=homeBubbleChanged)
    def homeBubble(self) -> LeafletPoly:
        return self._home_bubble

    @Property(list, notify=ipBubbleChanged)
    def ipBubble(self) -> LeafletPoly:
        return self._ip_bubble

    @Property(list, notify=permissibleZoneChanged)
    def permissibleZone(self) -> LeafletPoly:
        return self._permissible_zone

    @Property(list, notify=safeZonesChanged)
    def safeZones(self) -> list[LeafletPoly]:
        return self._safe_zones

    @classmethod
    def empty(cls) -> IpZonesJs:
        return IpZonesJs([], [], [], [])

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> IpZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return IpZonesJs.empty()
        target = flight.package.target
        home = flight.departure
        geometry = IpZoneGeometry(target.position, home.position, game.blue)
        return IpZonesJs(
            ShapelyUtil.poly_to_leaflet(geometry.home_bubble, game.theater),
            ShapelyUtil.poly_to_leaflet(geometry.ip_bubble, game.theater),
            ShapelyUtil.poly_to_leaflet(geometry.permissible_zone, game.theater),
            ShapelyUtil.polys_to_leaflet(geometry.safe_zones, game.theater),
        )
