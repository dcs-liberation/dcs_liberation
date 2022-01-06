from PySide2.QtCore import Property, QObject, Signal

from game.sim.combat.aircombat import AirCombat
from game.theater import ConflictTheater
from .leaflet import LeafletPoly
from .shapelyutil import ShapelyUtil


class AirCombatJs(QObject):
    footprintChanged = Signal()

    def __init__(self, combat: AirCombat, theater: ConflictTheater) -> None:
        super().__init__()
        self.combat = combat
        self.theater = theater
        self._footprint = self._make_footprint()

    @Property(type=list, notify=footprintChanged)
    def footprint(self) -> list[LeafletPoly]:
        return self._footprint

    def refresh(self) -> None:
        self._footprint = self._make_footprint()
        self.footprintChanged.emit()

    def _make_footprint(self) -> list[LeafletPoly]:
        return ShapelyUtil.polys_to_leaflet(self.combat.footprint, self.theater)
