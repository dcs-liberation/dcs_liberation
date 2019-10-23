from PySide2.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from gen.flights.flight import Flight
from game import Game
from qt_ui.windows.mission.flight.settings.QFlightDepartureEditor import QFlightDepartureEditor
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import QFlightTypeTaskInfo


class QGeneralFlightSettingsTab(QFrame):

    def __init__(self, flight: Flight, game: Game):
        super(QGeneralFlightSettingsTab, self).__init__()
        self.flight = flight
        self.game = game
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        self.flight_info = QFlightTypeTaskInfo(self.flight)
        self.flight_departure = QFlightDepartureEditor(self.flight)
        self.flight_slots = QFlightSlotEditor(self.flight, self.game)
        self.flight_start_type = QFlightStartType(self.flight)
        layout.addWidget(self.flight_info, 0, 0)
        layout.addWidget(self.flight_departure, 1, 0)
        layout.addWidget(self.flight_slots, 2, 0)
        layout.addWidget(self.flight_start_type, 3, 0)
        vstretch = QVBoxLayout()
        vstretch.addStretch()
        layout.addLayout(vstretch, 3, 0)
        self.setLayout(layout)

        self.flight_start_type.setEnabled(self.flight.client_count > 0)
        self.flight_slots.changed.connect(lambda: self.flight_start_type.setEnabled(self.flight.client_count > 0))
