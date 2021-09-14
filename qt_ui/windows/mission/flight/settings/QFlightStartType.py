from PySide2.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from game.ato.flight import Flight
from qt_ui.models import PackageModel


class QFlightStartType(QGroupBox):
    def __init__(self, package_model: PackageModel, flight: Flight):
        super().__init__()
        self.package_model = package_model
        self.flight = flight

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

    def _on_start_type_selected(self):
        selected = self.start_type.currentData()
        self.flight.start_type = selected
        self.package_model.update_tot()
