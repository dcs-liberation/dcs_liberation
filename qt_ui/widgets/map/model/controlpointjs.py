from __future__ import annotations

from typing import Optional

from PySide2.QtCore import Property, QObject, Signal, Slot
from dcs import Point

from game.theater import ConflictTheater, ControlPoint, ControlPointStatus, LatLon
from game.utils import meters, nautical_miles
from qt_ui.dialogs import Dialog
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from .leaflet import LeafletLatLon

MAX_SHIP_DISTANCE = nautical_miles(80)


class ControlPointJs(QObject):
    nameChanged = Signal()
    blueChanged = Signal()
    positionChanged = Signal()
    mobileChanged = Signal()
    destinationChanged = Signal(list)
    categoryChanged = Signal()
    statusChanged = Signal()

    def __init__(
        self,
        control_point: ControlPoint,
        game_model: GameModel,
        theater: ConflictTheater,
    ) -> None:
        super().__init__()
        self.control_point = control_point
        self.game_model = game_model
        self.theater = theater
        self.dialog: Optional[QBaseMenu2] = None

    @Property(str, notify=nameChanged)
    def name(self) -> str:
        return self.control_point.name

    @Property(bool, notify=blueChanged)
    def blue(self) -> bool:
        return self.control_point.captured

    @Property(str, notify=categoryChanged)
    def category(self) -> str:
        return self.control_point.category

    @Property(str, notify=statusChanged)
    def status(self) -> str:
        status = self.control_point.status
        if status is ControlPointStatus.Functional:
            return "alive"
        elif status is ControlPointStatus.Damaged:
            return "damaged"
        elif status is ControlPointStatus.Destroyed:
            return "destroyed"
        raise ValueError(f"Unhandled ControlPointStatus: {status.name}")

    @Property(list, notify=positionChanged)
    def position(self) -> LeafletLatLon:
        ll = self.theater.point_to_ll(self.control_point.position)
        return [ll.latitude, ll.longitude]

    @Property(bool, notify=mobileChanged)
    def mobile(self) -> bool:
        return self.control_point.moveable and self.control_point.captured

    @Property(list, notify=destinationChanged)
    def destination(self) -> LeafletLatLon:
        if self.control_point.target_position is None:
            # Qt seems to convert None to [] for list Properties :(
            return []
        return self.theater.point_to_ll(self.control_point.target_position).as_list()

    def destination_in_range(self, destination: Point) -> bool:
        move_distance = meters(
            destination.distance_to_point(self.control_point.position)
        )
        return move_distance <= MAX_SHIP_DISTANCE

    @Slot(list, result=bool)
    def destinationInRange(self, destination: LeafletLatLon) -> bool:
        return self.destination_in_range(self.theater.ll_to_point(LatLon(*destination)))

    @Slot(list, result=str)
    def setDestination(self, destination: LeafletLatLon) -> str:
        if not self.control_point.moveable:
            return f"{self.control_point} is not mobile"
        if not self.control_point.captured:
            return f"{self.control_point} is not owned by player"

        point = self.theater.ll_to_point(LatLon(*destination))
        if not self.destination_in_range(point):
            return (
                f"Cannot move {self.control_point} more than "
                f"{MAX_SHIP_DISTANCE.nautical_miles}nm."
            )
        self.control_point.target_position = point
        self.destinationChanged.emit(destination)
        return ""

    @Slot()
    def cancelTravel(self) -> None:
        self.control_point.target_position = None
        self.destinationChanged.emit([])

    @Slot()
    def showInfoDialog(self) -> None:
        if self.dialog is None:
            self.dialog = QBaseMenu2(None, self.control_point, self.game_model)
        self.dialog.show()

    @Slot()
    def showPackageDialog(self) -> None:
        Dialog.open_new_package_dialog(self.control_point)
