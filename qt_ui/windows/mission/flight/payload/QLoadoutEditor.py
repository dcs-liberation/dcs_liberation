from PySide2.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from game import Game
from game.data.weapons import Pylon
from game.ato.flight import Flight
from qt_ui.windows.mission.flight.payload.QPylonEditor import QPylonEditor


class QLoadoutEditor(QGroupBox):
    def __init__(self, flight: Flight, game: Game) -> None:
        super().__init__("Use custom loadout")
        self.flight = flight
        self.game = game
        self.setCheckable(True)
        self.setChecked(flight.loadout.is_custom)

        vbox = QVBoxLayout(self)
        layout = QGridLayout(self)

        for i, pylon in enumerate(Pylon.iter_pylons(self.flight.unit_type)):
            label = QLabel(f"<b>{pylon.number}</b>")
            label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            layout.addWidget(label, i, 0)
            layout.addWidget(QPylonEditor(game, flight, pylon), i, 1)

        vbox.addLayout(layout)
        vbox.addStretch()
        self.setLayout(vbox)

        for i in self.findChildren(QPylonEditor):
            i.set_from(self.flight.loadout)

    def reset_pylons(self) -> None:
        self.flight.use_custom_loadout = self.isChecked()
        if not self.isChecked():
            for i in self.findChildren(QPylonEditor):
                i.set_from(self.flight.loadout)
