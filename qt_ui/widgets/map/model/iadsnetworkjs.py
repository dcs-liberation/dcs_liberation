from __future__ import annotations

from PySide2.QtCore import Property, QObject, Signal
from game.theater import TheaterGroundObject
from game.theater.theatergroundobject import IadsBuildingGroundObject, IADSRole
from qt_ui.widgets.map.model.leaflet import LeafletPoly


class IadsConnectionJs(QObject):
    pointsChanged = Signal()

    def __init__(
        self,
        a: TheaterGroundObject,
        b: TheaterGroundObject,
        points: LeafletPoly,
    ) -> None:
        super().__init__()
        self.node_a = a
        self.node_b = b
        self._points = points

    @Property(bool)
    def blue(self) -> bool:
        return self.node_a.is_friendly(True)

    @Property(list, notify=pointsChanged)
    def points(self) -> LeafletPoly:
        return self._points

    @Property(bool)
    def is_power_connection(self) -> bool:
        return (
            isinstance(self.node_a, IadsBuildingGroundObject)
            and self.node_a.iads_role == IADSRole.PowerSource
        ) or (
            isinstance(self.node_b, IadsBuildingGroundObject)
            and self.node_b.iads_role == IADSRole.PowerSource
        )
