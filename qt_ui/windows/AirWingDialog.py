from typing import Optional

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    Qt,
    QSize,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QListView,
    QVBoxLayout,
)

from game import db
from game.squadrons import Squadron
from qt_ui.delegates import TwoColumnRowDelegate
from qt_ui.models import GameModel, AirWingModel, SquadronModel
from qt_ui.windows.SquadronDialog import SquadronDialog


class SquadronDelegate(TwoColumnRowDelegate):
    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__(rows=2, columns=2, font_size=12)
        self.air_wing_model = air_wing_model

    @staticmethod
    def squadron(index: QModelIndex) -> Squadron:
        return index.data(AirWingModel.SquadronRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        if (row, column) == (0, 0):
            return self.air_wing_model.data(index, Qt.DisplayRole)
        elif (row, column) == (0, 1):
            squadron = self.air_wing_model.data(index, AirWingModel.SquadronRole)
            return db.unit_get_expanded_info(
                squadron.country, squadron.aircraft, "name"
            )
        elif (row, column) == (1, 0):
            return self.squadron(index).nickname
        elif (row, column) == (1, 1):
            squadron = self.squadron(index)
            active = len(squadron.active_pilots)
            available = len(squadron.available_pilots)
            return f"{squadron.size} pilots, {active} active, {available} unassigned"
        return ""


class SquadronList(QListView):
    """List view for displaying the air wing's squadrons."""

    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__()
        self.air_wing_model = air_wing_model
        self.dialog: Optional[SquadronDialog] = None

        self.setIconSize(QSize(91, 24))
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
