from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from game import Game
from game.navmesh import NavMesh
from game.theater import ConflictTheater
from .leaflet import LeafletPoly
from .navmeshpolyjs import NavMeshPolyJs


class NavMeshJs(QObject):
    blueChanged = Signal()
    redChanged = Signal()

    def __init__(self, blue: list[NavMeshPolyJs], red: list[NavMeshPolyJs]) -> None:
        super().__init__()
        self._blue = blue
        self._red = red
        # TODO: Boundary markers.
        # TODO: Numbering.
        # TODO: Localization debugging.

    @Property(list, notify=blueChanged)
    def blue(self) -> list[LeafletPoly]:
        return self._blue

    @Property(list, notify=redChanged)
    def red(self) -> list[LeafletPoly]:
        return self._red

    @staticmethod
    def to_polys(navmesh: NavMesh, theater: ConflictTheater) -> list[NavMeshPolyJs]:
        polys = []
        for poly in navmesh.polys:
            polys.append(NavMeshPolyJs.from_navmesh(poly, theater))
        return polys

    @classmethod
    def from_game(cls, game: Game) -> NavMeshJs:
        return NavMeshJs(
            cls.to_polys(game.blue.nav_mesh, game.theater),
            cls.to_polys(game.red.nav_mesh, game.theater),
        )
