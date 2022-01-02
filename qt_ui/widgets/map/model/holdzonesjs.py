from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from game import Game
from game.ato import Flight
from game.flightplan import HoldZoneGeometry
from .config import ENABLE_EXPENSIVE_DEBUG_TOOLS
from .joinzonesjs import JoinZonesJs
from .leaflet import LeafletLatLon, LeafletPoly
from .shapelyutil import ShapelyUtil


class HoldZonesJs(QObject):
    homeBubbleChanged = Signal()
    targetBubbleChanged = Signal()
    joinBubbleChanged = Signal()
    excludedZonesChanged = Signal()
    permissibleZonesChanged = Signal()
    preferredLinesChanged = Signal()

    def __init__(
        self,
        home_bubble: LeafletPoly,
        target_bubble: LeafletPoly,
        join_bubble: LeafletPoly,
        excluded_zones: list[LeafletPoly],
        permissible_zones: list[LeafletPoly],
        preferred_lines: list[list[LeafletLatLon]],
    ) -> None:
        super().__init__()
        self._home_bubble = home_bubble
        self._target_bubble = target_bubble
        self._join_bubble = join_bubble
        self._excluded_zones = excluded_zones
        self._permissible_zones = permissible_zones
        self._preferred_lines = preferred_lines

    @Property(list, notify=homeBubbleChanged)
    def homeBubble(self) -> LeafletPoly:
        return self._home_bubble

    @Property(list, notify=targetBubbleChanged)
    def targetBubble(self) -> LeafletPoly:
        return self._target_bubble

    @Property(list, notify=joinBubbleChanged)
    def joinBubble(self) -> LeafletPoly:
        return self._join_bubble

    @Property(list, notify=excludedZonesChanged)
    def excludedZones(self) -> list[LeafletPoly]:
        return self._excluded_zones

    @Property(list, notify=permissibleZonesChanged)
    def permissibleZones(self) -> list[LeafletPoly]:
        return self._permissible_zones

    @Property(list, notify=preferredLinesChanged)
    def preferredLines(self) -> list[list[LeafletLatLon]]:
        return self._preferred_lines

    @classmethod
    def empty(cls) -> HoldZonesJs:
        return HoldZonesJs([], [], [], [], [], [])

    @classmethod
    def for_flight(cls, flight: Flight, game: Game) -> HoldZonesJs:
        if not ENABLE_EXPENSIVE_DEBUG_TOOLS:
            return JoinZonesJs.empty()
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
            ShapelyUtil.poly_to_leaflet(geometry.home_bubble, game.theater),
            ShapelyUtil.poly_to_leaflet(geometry.target_bubble, game.theater),
            ShapelyUtil.poly_to_leaflet(geometry.join_bubble, game.theater),
            ShapelyUtil.polys_to_leaflet(geometry.excluded_zones, game.theater),
            ShapelyUtil.polys_to_leaflet(geometry.permissible_zones, game.theater),
            ShapelyUtil.lines_to_leaflet(geometry.preferred_lines, game.theater),
        )
