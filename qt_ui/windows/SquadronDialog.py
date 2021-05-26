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

from game.squadrons import Pilot
from qt_ui.delegates import painter_context
from qt_ui.models import SquadronModel


class PilotDelegate(QStyledItemDelegate):
    FONT_SIZE = 10
    HMARGIN = 4
    VMARGIN = 4

    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__()
        self.squadron_model = squadron_model

    def get_font(self, option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setPointSize(self.FONT_SIZE)
        return font

    @staticmethod
    def pilot(index: QModelIndex) -> Pilot:
        return index.data(SquadronModel.PilotRole)

    def first_row_text(self, index: QModelIndex) -> str:
        return self.squadron_model.data(index, Qt.DisplayRole)

    def second_row_text(self, index: QModelIndex) -> str:
        return "Alive" if self.pilot(index).alive else "Dead"

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


class PilotList(QListView):
    """List view for displaying a squadron's pilots."""

    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__()
        self.squadron_model = squadron_model

        self.setItemDelegate(PilotDelegate(self.squadron_model))
        self.setModel(self.squadron_model)
        self.selectionModel().setCurrentIndex(
            self.squadron_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )

        # self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)


class SquadronDialog(QDialog):
    """Dialog window showing a squadron."""

    def __init__(self, squadron_model: SquadronModel, parent) -> None:
        super().__init__(parent)

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(squadron_model.squadron.name)
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(PilotList(squadron_model))
