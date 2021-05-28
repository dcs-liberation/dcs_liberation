from PySide2.QtCore import (
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    Qt,
)
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QDialog,
    QHBoxLayout,
    QListView,
    QMenu,
    QPushButton,
    QVBoxLayout,
)

from game.transfers import TransferOrder
from qt_ui.delegates import TwoColumnRowDelegate
from qt_ui.models import GameModel, TransferModel


class TransferDelegate(TwoColumnRowDelegate):
    def __init__(self, transfer_model: TransferModel) -> None:
        super().__init__(rows=2, columns=1, font_size=12)
        self.transfer_model = transfer_model

    @staticmethod
    def transfer(index: QModelIndex) -> TransferOrder:
        return index.data(TransferModel.TransferRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        if row == 0:
            return self.transfer_model.data(index, Qt.DisplayRole)
        elif row == 1:
            return self.transfer(index).description
        return ""


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
        return self.transfer_model.transfer_at_index(index).player

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        """Updates the state of the delete button."""
        if selected.empty():
            self.cancel_button.setEnabled(False)
            return
        self.cancel_button.setEnabled(self.can_cancel(selected.indexes()[0]))
