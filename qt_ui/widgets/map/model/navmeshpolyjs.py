from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal

from game.navmesh import NavMeshPoly
from game.theater import ConflictTheater
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class NavMeshPolyJs(QObject):
    polyChanged = Signal()
    threatenedChanged = Signal()

    def __init__(self, poly: LeafletPoly, threatened: bool) -> None:
        super().__init__()
        self._poly = poly
        self._threatened = threatened

    @Property(list, notify=polyChanged)
    def poly(self) -> LeafletPoly:
        return self._poly

    @Property(bool, notify=threatenedChanged)
    def threatened(self) -> bool:
        return self._threatened

    @classmethod
    def from_navmesh(cls, poly: NavMeshPoly, theater: ConflictTheater) -> NavMeshPolyJs:
        return NavMeshPolyJs(
            ShapelyUtil.poly_to_leaflet(poly.poly, theater), poly.threatened
        )
