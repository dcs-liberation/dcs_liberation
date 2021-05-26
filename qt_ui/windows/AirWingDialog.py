from typing import Optional

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
)
from PySide2.QtGui import QFont, QFontMetrics, QIcon, QPainter
from PySide2.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QListView,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QVBoxLayout,
)

from game.squadrons import Squadron
from qt_ui.delegates import painter_context
from qt_ui.models import GameModel, AirWingModel, SquadronModel
from qt_ui.windows.SquadronDialog import SquadronDialog


class SquadronDelegate(QStyledItemDelegate):
    FONT_SIZE = 10
    HMARGIN = 4
    VMARGIN = 4

    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__()
        self.air_wing_model = air_wing_model

    def get_font(self, option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setPointSize(self.FONT_SIZE)
        return font

    @staticmethod
    def squadron(index: QModelIndex) -> Squadron:
        return index.data(AirWingModel.SquadronRole)

    def first_row_text(self, index: QModelIndex) -> str:
        return self.air_wing_model.data(index, Qt.DisplayRole)

    def second_row_text(self, index: QModelIndex) -> str:
        return self.squadron(index).nickname

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        # Draw the list item with all the default selection styling, but with an
        # invalid index so text formatting is left to us.
        super().paint(painter, option, QModelIndex())

        rect = option.rect.adjusted(
            self.HMARGIN, self.VMARGIN, -self.HMARGIN, -self.VMARGIN
        )

        with painter_context(painter):
            painter.setFont(self.get_font(option))

            icon: Optional[QIcon] = index.data(Qt.DecorationRole)
            if icon is not None:
                icon.paint(
                    painter,
                    rect,
                    Qt.AlignLeft | Qt.AlignVCenter,
                    self.icon_mode(option),
                    self.icon_state(option),
                )

            rect = rect.adjusted(self.icon_size(option).width() + self.HMARGIN, 0, 0, 0)
            painter.drawText(rect, Qt.AlignLeft, self.first_row_text(index))
            line2 = rect.adjusted(0, rect.height() / 2, 0, rect.height() / 2)
            painter.drawText(line2, Qt.AlignLeft, self.second_row_text(index))

    @staticmethod
    def icon_mode(option: QStyleOptionViewItem) -> QIcon.Mode:
        if not (option.state & QStyle.State_Enabled):
            return QIcon.Disabled
        elif option.state & QStyle.State_Selected:
            return QIcon.Selected
        elif option.state & QStyle.State_Active:
            return QIcon.Active
        return QIcon.Normal

    @staticmethod
    def icon_state(option: QStyleOptionViewItem) -> QIcon.State:
        return QIcon.On if option.state & QStyle.State_Open else QIcon.Off

    @staticmethod
    def icon_size(option: QStyleOptionViewItem) -> QSize:
        icon_size: Optional[QSize] = option.decorationSize
        if icon_size is None:
            return QSize(0, 0)
        else:
            return icon_size

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        left = self.icon_size(option).width() + self.HMARGIN
        metrics = QFontMetrics(self.get_font(option))
        first = metrics.size(0, self.first_row_text(index))
        second = metrics.size(0, self.second_row_text(index))
        text_width = max(first.width(), second.width())
        return QSize(
            left + text_width + 2 * self.HMARGIN,
            first.height() + second.height() + 2 * self.VMARGIN,
        )


class SquadronList(QListView):
    """List view for displaying the air wing's squadrons."""

    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__()
        self.air_wing_model = air_wing_model
        self.dialog: Optional[SquadronDialog] = None

        self.setItemDelegate(SquadronDelegate(self.air_wing_model))
        self.setModel(self.air_wing_model)
        self.selectionModel().setCurrentIndex(
            self.air_wing_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )

        # self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.dialog = SquadronDialog(
            SquadronModel(self.air_wing_model.squadron_at_index(index)), self
        )
        self.dialog.show()


class AirWingDialog(QDialog):
    """Dialog window showing the player's air wing."""

    def __init__(self, game_model: GameModel, parent) -> None:
        super().__init__(parent)
        self.air_wing_model = game_model.blue_air_wing_model

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(f"Air Wing")
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(SquadronList(self.air_wing_model))
