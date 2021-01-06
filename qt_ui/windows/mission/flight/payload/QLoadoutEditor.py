from PySide2.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from game import Game
from game.data.weapons import Pylon
from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.payload.QPylonEditor import QPylonEditor


class QLoadoutEditor(QGroupBox):

    def __init__(self, flight: Flight, game: Game) -> None:
        super().__init__("Use custom loadout")
        self.flight = flight
        self.game = game
        self.setCheckable(True)
        self.setChecked(flight.use_custom_loadout)

        self.toggled.connect(self.on_toggle)

        hboxLayout = QVBoxLayout(self)
        layout = QGridLayout(self)

        for i, pylon in enumerate(Pylon.iter_pylons(self.flight.unit_type)):
            label = QLabel(f"<b>{pylon.number}</b>")
            label.setSizePolicy(
                QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            layout.addWidget(label, i, 0)
            layout.addWidget(QPylonEditor(game, flight, pylon), i, 1)

        hboxLayout.addLayout(layout)
        hboxLayout.addStretch()
        self.setLayout(hboxLayout)

    def on_toggle(self):
        self.flight.use_custom_loadout = self.isChecked()
        if not self.isChecked():
            for i in self.findChildren(QPylonEditor):
                for j in enumerate(Pylon.iter_pylons(self.flight.unit_type)):
                    # Only change the text in the pylon selector, not any actual data.
                    i.default_loadout(j[0])
        else:
            for i in self.findChildren(QPylonEditor):
                # Clear the loadout so that the user has select it themself.
                # If we don't do this, the user may end up leaving an entry as the default,
                # which is just text, not actual data, meaning they'd have an empty pylon.
                i.clear_loadout()
