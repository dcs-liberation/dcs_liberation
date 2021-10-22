from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from game import Game
from gen.flights.flight import Flight, FlightRoster
from qt_ui.models import PackageModel


class QFlightStartType(QGroupBox):
    def __init__(
        self,
        package_model: PackageModel,
        flight: Flight,
        game: Game,
        pilots_changed: Signal,
    ):
        super().__init__()
        self.package_model = package_model
        self.flight = flight
        self.game = game

        self.layout = QVBoxLayout()
        self.main_row = QHBoxLayout()
        self.start_type_label = QLabel("Start type:")
        self.start_type = QComboBox()

        for i, st in enumerate([b for b in ["Cold", "Warm", "Runway", "In Flight"]]):
            self.start_type.addItem(st, st)
            if flight.start_type == st:
                self.start_type.setCurrentIndex(i)

        self.start_type.currentTextChanged.connect(self._on_start_type_selected)
        self.main_row.addWidget(self.start_type_label)
        self.main_row.addWidget(self.start_type)

        self.layout.addLayout(self.main_row)
        self.layout.addWidget(
            QLabel(
                "Any option other than Cold will make this flight non-targetable "
                + "by OCA/Aircraft missions. This will affect game balance."
            )
        )
        self.setLayout(self.layout)

        pilots_changed.connect(self.on_pilot_selected)

    def on_pilot_selected(self):
        # Pilot selection detected. If this is a player flight, set start_type
        # as configured for players in the settings.
        # Otherwise, set the start_type as configured for AI.
        # https://github.com/dcs-liberation/dcs_liberation/issues/1567

        if self.flight.roster.player_count > 0:
            self.flight.start_type = self.game.settings.default_start_type_client
        else:
            self.flight.start_type = self.game.settings.default_start_type

        for i, st in enumerate([b for b in ["Cold", "Warm", "Runway", "In Flight"]]):
            if self.flight.start_type == st:
                self.start_type.setCurrentIndex(i)

        self.package_model.update_tot()

    def _on_start_type_selected(self):
        selected = self.start_type.currentData()
        self.flight.start_type = selected
        self.package_model.update_tot()
