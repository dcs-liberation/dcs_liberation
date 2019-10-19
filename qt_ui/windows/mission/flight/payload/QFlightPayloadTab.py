from PySide2.QtWidgets import QFrame, QGridLayout

from game import Game
from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.payload.QLoadoutEditor import QLoadoutEditor


class QFlightPayloadTab(QFrame):

    def __init__(self, flight: Flight, game: Game):
        super(QFlightPayloadTab, self).__init__()
        self.flight = flight
        self.payload_editor = QLoadoutEditor(flight, game)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(self.payload_editor)
        self.setLayout(layout)
