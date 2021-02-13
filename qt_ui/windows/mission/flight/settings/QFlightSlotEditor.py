import logging

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QLabel, QGroupBox, QSpinBox, QGridLayout

from game import Game
from gen.flights.flight import Flight
from qt_ui.models import PackageModel


class QFlightSlotEditor(QGroupBox):

    changed = Signal()

    def __init__(self, package_model: PackageModel, flight: Flight, game: Game):
        super().__init__("Slots")
        self.package_model = package_model
        self.flight = flight
        self.game = game
        self.inventory = self.game.aircraft_inventory.for_control_point(flight.from_cp)
        available = self.inventory.available(self.flight.unit_type)
        max_count = self.flight.count + available
        if max_count > 4:
            max_count = 4

        layout = QGridLayout()

        self.aircraft_count = QLabel("Aircraft count:")
        self.aircraft_count_spinner = QSpinBox()
        self.aircraft_count_spinner.setMinimum(1)
        self.aircraft_count_spinner.setMaximum(max_count)
        self.aircraft_count_spinner.setValue(flight.count)
        self.aircraft_count_spinner.valueChanged.connect(self._changed_aircraft_count)

        self.client_count = QLabel("Client slots count:")
        self.client_count_spinner = QSpinBox()
        self.client_count_spinner.setMinimum(0)
        self.client_count_spinner.setMaximum(max_count)
        self.client_count_spinner.setValue(flight.client_count)
        self.client_count_spinner.valueChanged.connect(self._changed_client_count)

        if not self.flight.unit_type.flyable:
            self.client_count_spinner.setValue(0)
            self.client_count_spinner.setEnabled(False)

        layout.addWidget(self.aircraft_count, 0, 0)
        layout.addWidget(self.aircraft_count_spinner, 0, 1)

        layout.addWidget(self.client_count, 1, 0)
        layout.addWidget(self.client_count_spinner, 1, 1)

        self.setLayout(layout)

    def _changed_aircraft_count(self):
        self.game.aircraft_inventory.return_from_flight(self.flight)
        old_count = self.flight.count
        self.flight.count = int(self.aircraft_count_spinner.value())
        try:
            self.game.aircraft_inventory.claim_for_flight(self.flight)
        except ValueError:
            # The UI should have prevented this, but if we ran out of aircraft
            # then roll back the inventory change.
            difference = self.flight.count - old_count
            available = self.inventory.available(self.flight.unit_type)
            logging.error(
                f"Could not add {difference} additional aircraft to "
                f"{self.flight} because {self.flight.from_cp} has only "
                f"{available} {self.flight.unit_type} remaining"
            )
            self.flight.count = old_count
            self.game.aircraft_inventory.claim_for_flight(self.flight)
        self.changed.emit()

    def _changed_client_count(self):
        self.flight.client_count = int(self.client_count_spinner.value())
        self._cap_client_count()
        self.package_model.update_tot()
        self.changed.emit()

    def _cap_client_count(self):
        if self.flight.client_count > self.flight.count:
            self.flight.client_count = self.flight.count
            self.client_count_spinner.setValue(self.flight.client_count)
