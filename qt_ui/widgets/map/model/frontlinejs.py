from __future__ import annotations

from typing import List

from PySide2.QtCore import Property, QObject, Signal, Slot

from game.theater import ConflictTheater, FrontLine
from game.utils import nautical_miles
from qt_ui.dialogs import Dialog
from .leaflet import LeafletLatLon


class FrontLineJs(QObject):
    extentsChanged = Signal()

    def __init__(self, front_line: FrontLine, theater: ConflictTheater) -> None:
        super().__init__()
        self.front_line = front_line
        self.theater = theater

    @Property(list, notify=extentsChanged)
    def extents(self) -> List[LeafletLatLon]:
        a = self.theater.point_to_ll(
            self.front_line.position.point_from_heading(
                self.front_line.attack_heading.right.degrees, nautical_miles(2).meters
            )
        )
        b = self.theater.point_to_ll(
            self.front_line.position.point_from_heading(
                self.front_line.attack_heading.left.degrees, nautical_miles(2).meters
            )
        )
        return [[a.latitude, a.longitude], [b.latitude, b.longitude]]

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.front_line)
