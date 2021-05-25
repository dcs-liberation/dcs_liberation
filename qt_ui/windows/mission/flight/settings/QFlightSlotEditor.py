import logging

from PySide2.QtCore import Signal, QModelIndex
from PySide2.QtWidgets import QLabel, QGroupBox, QSpinBox, QGridLayout, QComboBox

from game import Game
from gen.flights.flight import Flight
from qt_ui.models import PackageModel


class PilotSelector(QComboBox):
    available_pilots_changed = Signal()

    def __init__(self, flight: Flight, idx: int) -> None:
        super().__init__()
        self.flight = flight
        self.pilot_index = idx

        self.rebuild(initial_build=True)

    def _do_rebuild(self) -> None:
        self.clear()
        if self.pilot_index >= self.flight.count:
            self.addItem("No aircraft", None)
            self.setDisabled(True)
            return

        self.setEnabled(True)
        self.addItem("Unassigned", None)
        choices = list(self.flight.squadron.available_pilots)
        current_pilot = self.flight.pilots[self.pilot_index]
        if current_pilot is not None:
            choices.append(current_pilot)
        for pilot in sorted(choices, key=lambda p: p.name):
            self.addItem(pilot.name, pilot)
        if current_pilot is None:
            self.setCurrentText("Unassigned")
            return
        self.setCurrentText(current_pilot.name)
        self.currentIndexChanged.connect(self.replace_pilot)

    def rebuild(self, initial_build: bool = False) -> None:
        current_selection = self.currentData()

        # The contents of the selector depend on the selection of the other selectors
        # for the flight, so changing the selection of one causes each selector to
        # rebuild. A rebuild causes a selection change, so if we don't block signals
        # during a rebuild we'll never stop rebuilding. Block signals during the rebuild
        # and emit signals if anything actually changes afterwards.
        self.blockSignals(True)
        try:
            self._do_rebuild()
        finally:
            self.blockSignals(False)

        new_selection = self.currentData()
        if not initial_build and current_selection != new_selection:
            self.currentIndexChanged.emit(self.currentIndex())
            self.currentTextChanged.emit(self.currentText())

    def replace_pilot(self, index: QModelIndex) -> None:
        if self.itemText(index) == "No aircraft":
            # The roster resize is handled separately, so we have no pilots to remove.
            return
        pilot = self.itemData(index)
        if pilot == self.flight.pilots[self.pilot_index]:
            return
        self.flight.set_pilot(self.pilot_index, pilot)
        self.available_pilots_changed.emit()


class QFlightSlotEditor(QGroupBox):
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

        layout.addWidget(QLabel("Squadron:"), 2, 0)
        layout.addWidget(QLabel(self.flight.squadron.name), 2, 1)

        layout.addWidget(QLabel("Assigned pilots:"), 3, 0)
        self.pilot_selectors = []
        for pilot_idx, row in enumerate(range(3, 7)):
            selector = PilotSelector(self.flight, pilot_idx)
            selector.available_pilots_changed.connect(self.reset_pilot_selectors)
            self.pilot_selectors.append(selector)
            layout.addWidget(selector, row, 1)

        self.setLayout(layout)

    def reset_pilot_selectors(self) -> None:
        for selector in self.pilot_selectors:
            selector.rebuild()

    def _changed_aircraft_count(self):
        self.game.aircraft_inventory.return_from_flight(self.flight)
        new_count = int(self.aircraft_count_spinner.value())
        try:
            self.game.aircraft_inventory.claim_for_flight(self.flight)
        except ValueError:
            # The UI should have prevented this, but if we ran out of aircraft
            # then roll back the inventory change.
            difference = new_count - self.flight.count
            available = self.inventory.available(self.flight.unit_type)
            logging.error(
                f"Could not add {difference} additional aircraft to "
                f"{self.flight} because {self.flight.departure} has only "
                f"{available} {self.flight.unit_type} remaining"
            )
            self.game.aircraft_inventory.claim_for_flight(self.flight)
            return

        self.flight.resize(new_count)
        self._cap_client_count()
        self.reset_pilot_selectors()

    def _changed_client_count(self):
        self.flight.client_count = int(self.client_count_spinner.value())
        self._cap_client_count()
        self.package_model.update_tot()

    def _cap_client_count(self):
        if self.flight.client_count > self.flight.count:
            self.flight.client_count = self.flight.count
            self.client_count_spinner.setValue(self.flight.client_count)
