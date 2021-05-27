from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    Qt,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QListView,
    QVBoxLayout,
)

from game.squadrons import Pilot
from qt_ui.delegates import TwoColumnRowDelegate
from qt_ui.models import SquadronModel


class PilotDelegate(TwoColumnRowDelegate):
    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__(rows=2, columns=2, font_size=12)
        self.squadron_model = squadron_model

    @staticmethod
    def pilot(index: QModelIndex) -> Pilot:
        return index.data(SquadronModel.PilotRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        pilot = self.pilot(index)
        if (row, column) == (0, 0):
            return self.squadron_model.data(index, Qt.DisplayRole)
        elif (row, column) == (0, 1):
            flown = pilot.record.missions_flown
            missions = "missions" if flown != 1 else "mission"
            return f"{flown} {missions} flown"
        elif (row, column) == (1, 0):
            return "Player" if pilot.player else "AI"
        elif (row, column) == (1, 1):
            return "Alive" if pilot.alive else "Dead"
        return ""


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
