from functools import cached_property
from typing import List, Optional

from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
)

from game.theater import ControlPoint
from game.transfers import RoadTransferOrder
from qt_ui.uiconstants import COLORS


class SupplyRouteSegment(QGraphicsLineItem):
    def __init__(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        control_point_a: ControlPoint,
        control_point_b: ControlPoint,
        convoys: List[RoadTransferOrder],
        parent: Optional[QGraphicsItem] = None,
    ) -> None:
        super().__init__(x0, y0, x1, y1, parent)
        self.control_point_a = control_point_a
        self.control_point_b = control_point_b
        self.convoys = convoys
        self.setPen(self.make_pen())
        self.setToolTip(self.make_tooltip())
        self.setAcceptHoverEvents(True)

    @property
    def has_convoys(self) -> bool:
        return bool(self.convoys)

    @cached_property
    def convoy_size(self) -> int:
        return sum(sum(c.units.values()) for c in self.convoys)

    def make_tooltip(self) -> str:
        if not self.has_convoys:
            return "No convoys present on this supply route."
        units = "units" if self.convoy_size > 1 else "unit"

        return (
            f"{self.convoy_size} {units} transferring between {self.control_point_a} "
            f"and {self.control_point_b}."
        )

    @property
    def line_color(self) -> QColor:
        if self.control_point_a.front_is_active(self.control_point_b):
            return COLORS["red"]
        elif self.control_point_a.captured:
            return COLORS["dark_blue"]
        else:
            return COLORS["dark_red"]

    @property
    def line_style(self) -> Qt.PenStyle:
        if (
            self.control_point_a.front_is_active(self.control_point_b)
            or self.has_convoys
        ):
            return Qt.PenStyle.SolidLine
        return Qt.PenStyle.DotLine

    def make_pen(self) -> QPen:
        pen = QPen(brush=self.line_color)
        pen.setColor(self.line_color)
        pen.setStyle(self.line_style)
        pen.setWidth(6)
        return pen
