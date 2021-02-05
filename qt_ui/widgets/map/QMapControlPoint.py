from typing import Optional

from PySide2.QtGui import QColor, QPainter
from PySide2.QtWidgets import QAction, QMenu

import qt_ui.uiconstants as const
from game.theater import ControlPoint, NavalControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.QBaseMenu2 import QBaseMenu2
from .QMapObject import QMapObject
from ...displayoptions import DisplayOptions
from ...windows.GameUpdateSignal import GameUpdateSignal


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
        self.capture_action = QAction(
            f"CHEAT: Capture {self.control_point.name}")
        self.capture_action.triggered.connect(self.cheat_capture)

        self.move_action = QAction("Move")
        self.move_action.triggered.connect(self.move)

        self.cancel_move_action = QAction("Cancel Move")
        self.cancel_move_action.triggered.connect(self.cancel_move)

    def paint(self, painter, option, widget=None) -> None:
        if DisplayOptions.control_points:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(self.brush_color)
            painter.setPen(self.pen_color)

            if not self.control_point.runway_is_operational():
                painter.setBrush(const.COLORS["black"])
                painter.setPen(self.brush_color)

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

    def add_context_menu_actions(self, menu: QMenu) -> None:

        if self.control_point.moveable and self.control_point.captured:
            menu.addAction(self.move_action)
            if self.control_point.target_position is not None:
                menu.addAction(self.cancel_move_action)

        if self.control_point.is_fleet:
            return

        if self.control_point.captured:
            return

        for connected in self.control_point.connected_points:
            if connected.captured and self.game_model.game.settings.enable_base_capture_cheat:
                menu.addAction(self.capture_action)
                break

    def cheat_capture(self) -> None:
        self.control_point.capture(self.game_model.game, for_player=True)
        # Reinitialized ground planners and the like.
        self.game_model.game.initialize_turn()
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)

    def move(self):
        self.parent.setSelectedUnit(self)

    def cancel_move(self):
        self.control_point.target_position = None
        GameUpdateSignal.get_instance().updateGame(self.game_model.game)
    
    def open_new_package_dialog(self) -> None:
        """Extends the default packagedialog to redirect to base menu for red air base."""
        is_navy = isinstance(self.control_point, NavalControlPoint)
        if self.control_point.captured or is_navy:
            super().open_new_package_dialog()
            return
        self.on_click()
