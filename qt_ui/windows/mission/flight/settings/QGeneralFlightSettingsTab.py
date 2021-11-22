from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from game import Game
from game.ato.flight import Flight
from qt_ui.models import PackageModel
from qt_ui.windows.mission.flight.settings.FlightAirfieldDisplay import (
    FlightAirfieldDisplay,
)
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import (
    QFlightTypeTaskInfo,
)
from qt_ui.windows.mission.flight.settings.QCustomName import QFlightCustomName


class QGeneralFlightSettingsTab(QFrame):
    on_flight_settings_changed = Signal()

    def __init__(self, game: Game, package_model: PackageModel, flight: Flight):
        super().__init__()

        layout = QGridLayout()
        layout.addWidget(QFlightTypeTaskInfo(flight), 0, 0)
        layout.addWidget(FlightAirfieldDisplay(game, package_model, flight), 1, 0)
        layout.addWidget(QFlightSlotEditor(package_model, flight, game), 2, 0)
        layout.addWidget(QFlightStartType(package_model, flight), 3, 0)
        layout.addWidget(QFlightCustomName(flight), 4, 0)
        vstretch = QVBoxLayout()
        vstretch.addStretch()
        layout.addLayout(vstretch, 5, 0)
        self.setLayout(layout)
