from __future__ import annotations

from typing import Iterator

from PySide2.QtCore import Property, QObject, Signal

from game import Game
from .leaflet import LeafletLatLon


class UnculledZone(QObject):
    positionChanged = Signal()
    radiusChanged = Signal()

    def __init__(self, position: LeafletLatLon, radius: float) -> None:
        super().__init__()
        self._position = position
        self._radius = radius

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        return self._position

    @Property(float, notify=radiusChanged)
    def radius(self) -> float:
        return self._radius

    @classmethod
    def each_from_game(cls, game: Game) -> Iterator[UnculledZone]:
        for zone in game.get_culling_zones():
            ll = game.theater.point_to_ll(zone)
            yield UnculledZone(
                [ll.latitude, ll.longitude], game.settings.perf_culling_distance * 1000
            )
