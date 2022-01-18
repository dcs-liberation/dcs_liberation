from __future__ import annotations

from typing import List, Optional

from PySide2.QtCore import Property, QObject, Signal, Slot

from game import Game
from game.theater import TheaterGroundObject
from qt_ui.dialogs import Dialog
from qt_ui.widgets.map.model.leaflet import LeafletLatLon
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu


class GroundObjectJs(QObject):
    nameChanged = Signal()
    controlPointNameChanged = Signal()
    unitsChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    samThreatRangesChanged = Signal()
    samDetectionRangesChanged = Signal()
    categoryChanged = Signal()
    deadChanged = Signal()

    def __init__(self, tgo: TheaterGroundObject, game: Game) -> None:
        super().__init__()
        self.tgo = tgo
        self.game = game
        self.theater = game.theater
        self.dialog: Optional[QGroundObjectMenu] = None

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QGroundObjectMenu(
                None,
                self.tgo,
                self.tgo.control_point,
                self.game,
            )
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.tgo)

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.tgo.name

    @Property(str, notify=controlPointNameChanged)
    def controlPointName(self) -> str:
        return self.tgo.control_point.name

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.tgo.category

    @Property(list, notify=unitsChanged)
    def units(self) -> List[str]:
        return [unit.display_name for unit in self.tgo.units]

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.tgo.control_point.captured

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.tgo.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=deadChanged)
    def dead(self) -> bool:
        return not any(g.alive_units > 0 for g in self.tgo.groups)

    @Property(list, notify=samThreatRangesChanged)
    def samThreatRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            threat_range = self.tgo.threat_range(group)
            if threat_range:
                ranges.append(threat_range.meters)
        return ranges

    @Property(list, notify=samDetectionRangesChanged)
    def samDetectionRanges(self) -> List[float]:
        if not self.tgo.might_have_aa:
            return []

        ranges = []
        for group in self.tgo.groups:
            detection_range = self.tgo.detection_range(group)
            if detection_range:
                ranges.append(detection_range.meters)
        return ranges
