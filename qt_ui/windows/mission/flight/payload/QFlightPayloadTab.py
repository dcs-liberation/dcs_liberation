from PySide2.QtCore import Qt
from PySide2.QtWidgets import QFrame, QLabel, QVBoxLayout

from game import Game
from gen.flights.flight import Flight
from gen.flights.loadouts import Loadout
from qt_ui.windows.mission.flight.payload.QLoadoutEditor import QLoadoutEditor


class QFlightPayloadTab(QFrame):
    def __init__(self, flight: Flight, game: Game):
        super(QFlightPayloadTab, self).__init__()
        self.flight = flight
        self.payload_editor = QLoadoutEditor(flight, game)

        layout = QVBoxLayout()

        # Docs Link
        docsText = QLabel(
            '<a href="https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Loadouts"><span style="color:#FFFFFF;">How to create your own default loadout</span></a>'
        )
        docsText.setAlignment(Qt.AlignCenter)
        docsText.setOpenExternalLinks(True)

        self.payload_editor.toggled.connect(self.on_custom_toggled)
        layout.addWidget(self.payload_editor)
        layout.addWidget(docsText)

        self.setLayout(layout)

    def on_custom_toggled(self, use_custom: bool) -> None:
        if use_custom:
            self.flight.loadout = self.flight.loadout.derive_custom("Custom")
        else:
            self.flight.loadout = Loadout.default_for(self.flight)
            self.payload_editor.reset_pylons()
