from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from game import Game
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class MapZonesJs(QObject):
    inclusionZonesChanged = Signal()
    exclusionZonesChanged = Signal()
    seaZonesChanged = Signal()

    def __init__(
        self,
        inclusion_zones: list[LeafletPoly],
        exclusion_zones: list[LeafletPoly],
        sea_zones: list[LeafletPoly],
    ) -> None:
        super().__init__()
        self._inclusion_zones = inclusion_zones
        self._exclusion_zones = exclusion_zones
        self._sea_zones = sea_zones

    @Property(list, notify=inclusionZonesChanged)
    def inclusionZones(self) -> list[LeafletPoly]:
        return self._inclusion_zones

    @Property(list, notify=exclusionZonesChanged)
    def exclusionZones(self) -> list[LeafletPoly]:
        return self._exclusion_zones

    @Property(list, notify=seaZonesChanged)
    def seaZones(self) -> list[LeafletPoly]:
        return self._sea_zones

    @classmethod
    def from_game(cls, game: Game) -> MapZonesJs:
        zones = game.theater.landmap
        return MapZonesJs(
            ShapelyUtil.polys_to_leaflet(zones.inclusion_zones, game.theater),
            ShapelyUtil.polys_to_leaflet(zones.exclusion_zones, game.theater),
            ShapelyUtil.polys_to_leaflet(zones.sea_zones, game.theater),
        )
