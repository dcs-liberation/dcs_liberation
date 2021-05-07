from PySide2.QtWidgets import QFrame, QGridLayout, QLabel
from PySide2.QtCore import Qt

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

        # Docs Link
        docsText = QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Loadouts"><span style="color:#FFFFFF;">How to create your own default loadout</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        layout.addWidget(self.payload_editor)
        layout.addWidget(docsText)

        self.setLayout(layout)
