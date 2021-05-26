from typing import Optional

from PySide2.QtCore import (
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
)
from PySide2.QtGui import QContextMenuEvent, QFont, QFontMetrics, QIcon, QPainter
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QDialog,
    QHBoxLayout,
    QListView,
    QMenu,
    QPushButton,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
    QVBoxLayout,
)

from game.transfers import TransferOrder
from qt_ui.delegates import painter_context
from qt_ui.models import GameModel, TransferModel


class TransferDelegate(QStyledItemDelegate):
    FONT_SIZE = 10
    HMARGIN = 4
    VMARGIN = 4

    def __init__(self, transfer_model: TransferModel) -> None:
        super().__init__()
        self.transfer_model = transfer_model

    def get_font(self, option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setPointSize(self.FONT_SIZE)
        return font

    @staticmethod
    def transfer(index: QModelIndex) -> TransferOrder:
        return index.data(TransferModel.TransferRole)

    def first_row_text(self, index: QModelIndex) -> str:
        return self.transfer_model.data(index, Qt.DisplayRole)

    def second_row_text(self, index: QModelIndex) -> str:
        return self.transfer(index).description

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


class PendingTransfersList(QListView):
    """List view for displaying the pending unit transfers."""

    def __init__(self, transfer_model: TransferModel) -> None:
        super().__init__()
        self.transfer_model = transfer_model

        self.setItemDelegate(TransferDelegate(self.transfer_model))
        self.setModel(self.transfer_model)
        self.selectionModel().setCurrentIndex(
            self.transfer_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )

        # self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        index = self.indexAt(event.pos())
        if not index.isValid():
            return
        if not self.transfer_model.transfer_at_index(index).player:
            return

        menu = QMenu("Menu")

        delete_action = QAction("Cancel")
        delete_action.triggered.connect(lambda: self.cancel_transfer(index))
        menu.addAction(delete_action)

        menu.exec_(event.globalPos())

    def cancel_transfer(self, index: QModelIndex) -> None:
        """Cancels the given transfer order."""
        self.transfer_model.cancel_transfer_at_index(index)


class PendingTransfersDialog(QDialog):
    """Dialog window showing all scheduled transfers for the player."""

    def __init__(self, game_model: GameModel, parent=None) -> None:
        super().__init__(parent)
        self.transfer_model = game_model.transfer_model

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(f"Pending Transfers")
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.transfer_list = PendingTransfersList(self.transfer_model)
        self.transfer_list.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        layout.addWidget(self.transfer_list)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        button_layout.addStretch()

        self.cancel_button = QPushButton("Cancel Transfer")
        self.cancel_button.setProperty("style", "btn-danger")
        self.cancel_button.clicked.connect(self.on_cancel_transfer)
        self.cancel_button.setEnabled(
            self.can_cancel(self.transfer_list.currentIndex())
        )
        button_layout.addWidget(self.cancel_button)

    def on_cancel_transfer(self) -> None:
        """Cancels the selected transfer order."""
        self.transfer_model.cancel_transfer_at_index(self.transfer_list.currentIndex())

    def can_cancel(self, index: QModelIndex) -> bool:
        if not index.isValid():
            return False
        return self.transfer_model.pilot_at_index(index).player

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        """Updates the state of the delete button."""
        if selected.empty():
            self.cancel_button.setEnabled(False)
            return
        self.cancel_button.setEnabled(self.can_cancel(selected.indexes()[0]))
