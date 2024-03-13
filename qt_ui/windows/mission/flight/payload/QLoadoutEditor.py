from collections.abc import Iterator

from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from game import Game
from game.ato.flight import Flight
from game.ato.flightmember import FlightMember
from game.data.weapons import Pylon
from qt_ui.blocksignals import block_signals
from qt_ui.windows.mission.flight.payload.QPylonEditor import QPylonEditor


class QLoadoutEditor(QGroupBox):
    def __init__(self, flight: Flight, flight_member: FlightMember, game: Game) -> None:
        super().__init__("Use custom loadout")
        self.flight = flight
        self.flight_member = flight_member
        self.game = game
        self.setCheckable(True)
        self.setChecked(flight_member.loadout.is_custom)

        vbox = QVBoxLayout(self)
        layout = QGridLayout(self)

        for i, pylon in enumerate(Pylon.iter_pylons(self.flight.unit_type)):
            label = QLabel(f"<b>{pylon.number}</b>")
            label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
            layout.addWidget(label, i, 0)
            layout.addWidget(QPylonEditor(game, flight, flight_member, pylon), i, 1)

        vbox.addLayout(layout)
        vbox.addStretch()
        self.setLayout(vbox)

        for pylon_editor in self.iter_pylon_editors():
            pylon_editor.set_from(self.flight_member.loadout)

    def iter_pylon_editors(self) -> Iterator[QPylonEditor]:
        yield from self.findChildren(QPylonEditor)

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        with block_signals(self):
            self.setChecked(self.flight_member.use_custom_loadout)
        for pylon_editor in self.iter_pylon_editors():
            pylon_editor.set_flight_member(flight_member)

    def reset_pylons(self) -> None:
        self.flight_member.use_custom_loadout = self.isChecked()
        if not self.isChecked():
            for pylon_editor in self.iter_pylon_editors():
                pylon_editor.set_from(self.flight_member.loadout)
