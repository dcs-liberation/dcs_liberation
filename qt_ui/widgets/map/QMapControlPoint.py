from typing import Optional

from PySide2.QtGui import QColor, QPainter

import qt_ui.uiconstants as const
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from theater import ControlPoint
from .QMapObject import QMapObject


class QMapControlPoint(QMapObject):
    def __init__(self, parent, x: float, y: float, w: float, h: float,
                 control_point: ControlPoint, game_model: GameModel) -> None:
        super().__init__(x, y, w, h, mission_target=control_point)
        self.game_model = game_model
        self.control_point = control_point
        self.parent = parent
        self.setZValue(1)
        self.setToolTip(self.control_point.name)
        self.base_details_dialog: Optional[QBaseMenu2] = None

    def paint(self, painter, option, widget=None) -> None:
        if self.parent.get_display_rule("cp"):
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(self.brush_color)
            painter.setPen(self.pen_color)

            if self.control_point.has_runway():
                if self.isUnderMouse():
                    painter.setBrush(const.COLORS["white"])
                    painter.setPen(self.pen_color)

                r = option.rect
                painter.drawEllipse(r.x(), r.y(), r.width(), r.height())
            # TODO: Draw sunk carriers differently.
            # Either don't draw them at all, or perhaps use a sunk ship icon.
            painter.restore()

    @property
    def brush_color(self) -> QColor:
        if self.control_point.captured:
            return const.COLORS["blue"]
        else:
            return const.COLORS["super_red"]

    @property
    def pen_color(self) -> QColor:
        return const.COLORS["white"]

    @property
    def object_dialog_text(self) -> str:
        if self.control_point.captured:
            return "Open base menu"
        else:
            return "Open intel menu"

    def on_click(self) -> None:
        self.base_details_dialog = QBaseMenu2(
            self.window(),
            self.control_point,
            self.game_model
        )
        self.base_details_dialog.show()
