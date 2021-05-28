import logging
from typing import Optional, Callable

from PySide2.QtCore import Signal, QModelIndex
from PySide2.QtWidgets import (
    QLabel,
    QGroupBox,
    QSpinBox,
    QGridLayout,
    QComboBox,
    QHBoxLayout,
    QCheckBox,
    QVBoxLayout,
)

from game import Game
from game.squadrons import Pilot
from gen.flights.flight import Flight
from qt_ui.models import PackageModel


class PilotSelector(QComboBox):
    available_pilots_changed = Signal()

    def __init__(self, flight: Flight, idx: int) -> None:
        super().__init__()
        self.flight = flight
        self.pilot_index = idx
        self.rebuild()

    @staticmethod
    def text_for(pilot: Pilot) -> str:
        return pilot.name

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
        # Put players first, otherwise alphabetically.
        for pilot in sorted(choices, key=lambda p: (not p.player, p.name)):
            self.addItem(self.text_for(pilot), pilot)
        if current_pilot is None:
            self.setCurrentText("Unassigned")
        else:
            self.setCurrentText(self.text_for(current_pilot))
        self.currentIndexChanged.connect(self.replace_pilot)

    def rebuild(self) -> None:
        # The contents of the selector depend on the selection of the other selectors
        # for the flight, so changing the selection of one causes each selector to
        # rebuild. A rebuild causes a selection change, so if we don't block signals
        # during a rebuild we'll never stop rebuilding.
        self.blockSignals(True)
        try:
            self._do_rebuild()
        finally:
            self.blockSignals(False)

    def replace_pilot(self, index: QModelIndex) -> None:
        if self.itemText(index) == "No aircraft":
            # The roster resize is handled separately, so we have no pilots to remove.
            return
        pilot = self.itemData(index)
        if pilot == self.flight.pilots[self.pilot_index]:
            return
        self.flight.set_pilot(self.pilot_index, pilot)
        self.available_pilots_changed.emit()


class PilotControls(QHBoxLayout):
    def __init__(self, flight: Flight, idx: int) -> None:
        super().__init__()
        self.flight = flight
        self.pilot_index = idx

        self.selector = PilotSelector(flight, idx)
        self.selector.currentIndexChanged.connect(self.on_pilot_changed)
        self.addWidget(self.selector)

        self.player_checkbox = QCheckBox()
        self.player_checkbox.setToolTip("Checked if this pilot is a player.")
        self.on_pilot_changed(self.selector.currentIndex())
        self.addWidget(self.player_checkbox)

        self.player_checkbox.toggled.connect(self.on_player_toggled)

    @property
    def pilot(self) -> Optional[Pilot]:
        if self.pilot_index >= self.flight.count:
            return None
        return self.flight.pilots[self.pilot_index]

    def on_player_toggled(self, checked: bool) -> None:
        pilot = self.pilot
        if pilot is None:
            logging.error("Cannot toggle state of a pilot when none is selected")
            return
        pilot.player = checked

    def on_pilot_changed(self, index: int) -> None:
        pilot = self.selector.itemData(index)
        self.player_checkbox.blockSignals(True)
        try:
            self.player_checkbox.setChecked(pilot is not None and pilot.player)
        finally:
            self.player_checkbox.blockSignals(False)

    def update_available_pilots(self) -> None:
        self.selector.rebuild()

    def enable_and_reset(self) -> None:
        self.selector.rebuild()
        self.on_pilot_changed(self.selector.currentIndex())

    def disable_and_clear(self) -> None:
        self.selector.rebuild()
        self.player_checkbox.blockSignals(True)
        try:
            self.player_checkbox.setEnabled(False)
            self.player_checkbox.setChecked(False)
        finally:
            self.player_checkbox.blockSignals(False)


class FlightRosterEditor(QVBoxLayout):
    MAX_PILOTS = 4

    def __init__(self, flight: Flight) -> None:
        super().__init__()

        self.pilot_controls = []
        for pilot_idx in range(self.MAX_PILOTS):

            def make_reset_callback(source_idx: int) -> Callable[[int], None]:
                def callback() -> None:
                    self.update_available_pilots(source_idx)

                return callback

            controls = PilotControls(flight, pilot_idx)
            controls.selector.available_pilots_changed.connect(
                make_reset_callback(pilot_idx)
            )
            self.pilot_controls.append(controls)
            self.addLayout(controls)

    def update_available_pilots(self, source_idx: int) -> None:
        for idx, controls in enumerate(self.pilot_controls):
            # No need to reset the source of the reset, it was just manually selected.
            if idx != source_idx:
                controls.update_available_pilots()

    def resize(self, new_size: int) -> None:
        if new_size > self.MAX_PILOTS:
            raise ValueError("A flight may not have more than four pilots.")
        for controls in self.pilot_controls[:new_size]:
            controls.enable_and_reset()
        for controls in self.pilot_controls[new_size:]:
            controls.disable_and_clear()


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

        layout.addWidget(self.aircraft_count, 0, 0)
        layout.addWidget(self.aircraft_count_spinner, 0, 1)

        layout.addWidget(QLabel("Squadron:"), 1, 0)
        layout.addWidget(QLabel(str(self.flight.squadron)), 1, 1)

        layout.addWidget(QLabel("Assigned pilots:"), 2, 0)
        self.roster_editor = FlightRosterEditor(flight)
        layout.addLayout(self.roster_editor, 2, 1)

        self.setLayout(layout)

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
        self.roster_editor.resize(new_count)
