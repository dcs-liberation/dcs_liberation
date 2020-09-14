from typing import Optional

from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import (
    QAction,
    QGraphicsSceneContextMenuEvent,
    QMenu,
)

import qt_ui.uiconstants as const
from game import Game
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from theater import ControlPoint
from .QMapObject import QMapObject


class QMapControlPoint(QMapObject):

    def __init__(self, parent, x: float, y: float, w: float, h: float,
                 model: ControlPoint, game: Game) -> None:
        super().__init__(x, y, w, h)
        self.model = model
        self.game = game
        self.parent = parent
        self.setZValue(1)
        self.setToolTip(self.model.name)
        self.base_details_dialog: Optional[QBaseMenu2] = None

    def paint(self, painter, option, widget=None) -> None:
        if self.parent.get_display_rule("cp"):
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(self.brush_color)
            painter.setPen(self.pen_color)

            if self.model.has_runway():
                if self.isUnderMouse():
                    painter.setBrush(const.COLORS["white"])
                    painter.setPen(self.pen_color)

                r = option.rect
                painter.drawEllipse(r.x(), r.y(), r.width(), r.height())
            # TODO: Draw sunk carriers differently.
            # Either don't draw them at all, or perhaps use a sunk ship icon.
            painter.restore()

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        if self.model.captured:
            text = "Open base menu"
        else:
            text = "Open intel menu"

        open_menu = QAction(text)
        open_menu.triggered.connect(self.on_click)

        menu = QMenu("Menu", self.parent)
        menu.addAction(open_menu)
        menu.exec_(event.screenPos())

    @property
    def brush_color(self) -> QColor:
        if self.model.captured:
            return const.COLORS["blue"]
        else:
            return const.COLORS["super_red"]

    @property
    def pen_color(self) -> QColor:
        return const.COLORS["white"]

    def on_click(self) -> None:
        self.base_details_dialog = QBaseMenu2(
            self.window(),
            self.model,
            self.game
        )
        self.base_details_dialog.show()
