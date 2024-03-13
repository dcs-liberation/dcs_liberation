from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from game import Game
from game.ato.flight import Flight
from qt_ui.models import PackageModel
from qt_ui.windows.mission.flight.settings.FlightPlanPropertiesGroup import (
    FlightPlanPropertiesGroup,
)
from qt_ui.windows.mission.flight.settings.QCustomName import QFlightCustomName
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import (
    QFlightTypeTaskInfo,
)


class QGeneralFlightSettingsTab(QFrame):
    flight_size_changed = Signal()

    def __init__(self, game: Game, package_model: PackageModel, flight: Flight):
        super().__init__()

        layout = QGridLayout()
        layout.addWidget(QFlightTypeTaskInfo(flight), 0, 0)
        layout.addWidget(FlightPlanPropertiesGroup(game, package_model, flight), 1, 0)
        self.flight_slot_editor = QFlightSlotEditor(package_model, flight, game)
        self.flight_slot_editor.flight_resized.connect(self.flight_size_changed)
        layout.addWidget(self.flight_slot_editor, 2, 0)
        layout.addWidget(QFlightStartType(package_model, flight), 3, 0)
        layout.addWidget(QFlightCustomName(flight), 4, 0)
        vstretch = QVBoxLayout()
        vstretch.addStretch()
        layout.addLayout(vstretch, 5, 0)
        self.setLayout(layout)
