import logging
from typing import Callable

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    Qt,
    QItemSelection,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QListView,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QCheckBox,
)

from game.squadrons import Pilot
from gen.flights.flight import FlightType
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
            return pilot.status.value
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


class AutoAssignedTaskControls(QVBoxLayout):
    def __init__(self, squadron_model: SquadronModel) -> None:
        super().__init__()
        self.squadron_model = squadron_model

        self.addWidget(QLabel("Auto-assignable mission types"))

        def make_callback(toggled_task: FlightType) -> Callable[[bool], None]:
            def callback(checked: bool) -> None:
                self.on_toggled(toggled_task, checked)

            return callback

        for task in squadron_model.squadron.mission_types:
            checkbox = QCheckBox(text=task.value)
            checkbox.setChecked(squadron_model.is_auto_assignable(task))
            checkbox.toggled.connect(make_callback(task))
            self.addWidget(checkbox)

        self.addStretch()

    def on_toggled(self, task: FlightType, checked: bool) -> None:
        self.squadron_model.set_auto_assignable(task, checked)


class SquadronDialog(QDialog):
    """Dialog window showing a squadron."""

    def __init__(self, squadron_model: SquadronModel, parent) -> None:
        super().__init__(parent)
        self.squadron_model = squadron_model

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(str(squadron_model.squadron))
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        columns = QHBoxLayout()
        layout.addLayout(columns)

        auto_assigned_tasks = AutoAssignedTaskControls(squadron_model)
        columns.addLayout(auto_assigned_tasks)

        self.pilot_list = PilotList(squadron_model)
        self.pilot_list.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        columns.addWidget(self.pilot_list)

        button_panel = QHBoxLayout()
        button_panel.addStretch()
        layout.addLayout(button_panel)

        self.toggle_ai_button = QPushButton()
        self.reset_ai_toggle_state(self.pilot_list.currentIndex())
        self.toggle_ai_button.setProperty("style", "start-button")
        self.toggle_ai_button.clicked.connect(self.toggle_ai)
        button_panel.addWidget(self.toggle_ai_button, alignment=Qt.AlignRight)

        self.toggle_leave_button = QPushButton()
        self.reset_leave_toggle_state(self.pilot_list.currentIndex())
        self.toggle_leave_button.setProperty("style", "start-button")
        self.toggle_leave_button.clicked.connect(self.toggle_leave)
        button_panel.addWidget(self.toggle_leave_button, alignment=Qt.AlignRight)

    def check_disabled_button_states(
        self, button: QPushButton, index: QModelIndex
    ) -> bool:
        if not index.isValid():
            button.setText("No pilot selected")
            button.setDisabled(True)
            return True
        pilot = self.squadron_model.pilot_at_index(index)
        if not pilot.alive:
            button.setText("Pilot is dead")
            button.setDisabled(True)
            return True
        return False

    def toggle_ai(self) -> None:
        index = self.pilot_list.currentIndex()
        if not index.isValid():
            logging.error("Cannot toggle player/AI: no pilot is selected")
            return
        self.squadron_model.toggle_ai_state(index)

    def reset_ai_toggle_state(self, index: QModelIndex) -> None:
        if self.check_disabled_button_states(self.toggle_ai_button, index):
            return
        if not self.squadron_model.squadron.aircraft.flyable:
            self.toggle_ai_button.setText("Not flyable")
            self.toggle_ai_button.setDisabled(True)
            return
        self.toggle_ai_button.setEnabled(True)
        pilot = self.squadron_model.pilot_at_index(index)
        self.toggle_ai_button.setText(
            "Convert to AI" if pilot.player else "Convert to player"
        )

    def toggle_leave(self) -> None:
        index = self.pilot_list.currentIndex()
        if not index.isValid():
            logging.error("Cannot toggle on leave state: no pilot is selected")
            return
        self.squadron_model.toggle_leave_state(index)

    def reset_leave_toggle_state(self, index: QModelIndex) -> None:
        if self.check_disabled_button_states(self.toggle_leave_button, index):
            return
        pilot = self.squadron_model.pilot_at_index(index)
        self.toggle_leave_button.setEnabled(
            not pilot.on_leave or self.squadron_model.squadron.has_unfilled_pilot_slots
        )
        self.toggle_leave_button.setText(
            "Return from leave" if pilot.on_leave else "Send on leave"
        )

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        index = selected.indexes()[0]
        self.reset_ai_toggle_state(index)
        self.reset_leave_toggle_state(index)
