from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from game import Game
from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.settings.QFlightDepartureEditor import QFlightDepartureEditor
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import QFlightTypeTaskInfo


class QGeneralFlightSettingsTab(QFrame):
    on_flight_settings_changed = Signal()

    def __init__(self, flight: Flight, game: Game, planner):
        super(QGeneralFlightSettingsTab, self).__init__()
        self.flight = flight
        self.game = game
        self.planner = planner
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        flight_info = QFlightTypeTaskInfo(self.flight)
        flight_departure = QFlightDepartureEditor(self.flight)
        flight_slots = QFlightSlotEditor(self.flight, self.game, self.planner)
        flight_start_type = QFlightStartType(self.flight)
        layout.addWidget(flight_info, 0, 0)
        layout.addWidget(flight_departure, 1, 0)
        layout.addWidget(flight_slots, 2, 0)
        layout.addWidget(flight_start_type, 3, 0)
        vstretch = QVBoxLayout()
        vstretch.addStretch()
        layout.addLayout(vstretch, 3, 0)
        self.setLayout(layout)

        flight_start_type.setEnabled(self.flight.client_count > 0)
        flight_slots.changed.connect(lambda: flight_start_type.setEnabled(self.flight.client_count > 0))
        flight_departure.changed.connect(lambda: self.on_flight_settings_changed.emit())
