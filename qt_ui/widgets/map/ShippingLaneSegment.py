from typing import List, Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
)

from game.theater import ControlPoint
from game.transfers import CargoShip
from qt_ui.uiconstants import COLORS


class ShippingLaneSegment(QGraphicsLineItem):
    def __init__(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        control_point_a: ControlPoint,
        control_point_b: ControlPoint,
        ships: List[CargoShip],
        parent: Optional[QGraphicsItem] = None,
    ) -> None:
        super().__init__(x0, y0, x1, y1, parent)
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b
        self.ships = ships
        self.setPen(self.make_pen())
        self.setToolTip(self.make_tooltip())
        self.setAcceptHoverEvents(True)

    @property
    def has_ships(self) -> bool:
        return bool(self.ships)

    def make_tooltip(self) -> str:
        if not self.has_ships:
            return "No ships present in this shipping lane."

        ships = []
        for ship in self.ships:
            units = "units" if ship.size > 1 else "unit"
            ships.append(
                f"{ship.size} {units} transferring from {ship.origin} to "
                f"{ship.destination}."
            )
        return "\n".join(ships)

    @property
    def line_color(self) -> QColor:
        if self.control_point_a.captured:
            return COLORS["dark_blue"]
        else:
            return COLORS["dark_red"]

    @property
    def line_style(self) -> Qt.PenStyle:
        if self.has_ships:
            return Qt.PenStyle.SolidLine
        return Qt.PenStyle.DotLine

    def make_pen(self) -> QPen:
        pen = QPen(brush=self.line_color)
        pen.setColor(self.line_color)
        pen.setStyle(self.line_style)
        pen.setWidth(2)
        return pen
