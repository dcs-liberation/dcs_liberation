from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from game import Game
from game.ato.flight import Flight, FlightRoster
from game.ato.starttype import StartType
from qt_ui.models import PackageModel
from game.ato.starttype import StartType


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
        self.start_type_combobox_label = QLabel("Start type:")
        self.start_type_combobox = QComboBox()

        default_start_type_str = (
            "Default (" + game.settings.default_start_type.value + ")"
        )
        self.start_type_combobox.addItem(default_start_type_str, None)
        for start_type in StartType:
            self.start_type_combobox.addItem(start_type.value, start_type)
        if flight.get_start_type is not None:
            self.start_type_combobox.setCurrentText(
                StartType(flight.get_start_type).value
            )
        else:
            self.start_type_combobox.setCurrentText(default_start_type_str)

        self.start_type_combobox.currentTextChanged.connect(
            self._on_start_type_selected
        )
        self.main_row.addWidget(self.start_type_combobox_label)
        self.main_row.addWidget(self.start_type_combobox)

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

        if self.start_type_combobox.currentData() is None:
            if self.flight.roster.player_count > 0:
                start_type = self.game.settings.default_start_type_client
            else:
                start_type = self.game.settings.default_start_type

            self.start_type_combobox.setCurrentText(
                "Default (" + start_type.value + ")"
            )

        self.package_model.update_tot()

    def _on_start_type_selected(self):
        selected = self.start_type_combobox.currentData()
        if selected is not None:
            self.flight.custom_start_type = StartType(selected)
        else:
            self.flight.custom_start_type = None
        self.package_model.update_tot()
