from re import L
from typing import Optional

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (
    QDialog,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
)
from dcs.planes import PlaneType

from game import Game
from game.theater import ControlPoint, OffMapSpawn
from gen.ato import Package
from gen.flights.flight import Flight
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QFlightSizeSpinner import QFlightSizeSpinner
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.combos.QAircraftTypeSelector import QAircraftTypeSelector
from qt_ui.widgets.combos.QArrivalAirfieldSelector import \
    QArrivalAirfieldSelector
from qt_ui.widgets.combos.QFlightTypeComboBox import QFlightTypeComboBox
from qt_ui.widgets.combos.QOriginAirfieldSelector import QOriginAirfieldSelector


class QFlightCreator(QDialog):
    created = Signal(Flight)

    def __init__(self, game: Game, package: Package, parent=None) -> None:
        super().__init__(parent=parent)

        self.game = game
        self.package = package
        self.custom_name_text = None
        self.country = self.game.player_country

        self.setWindowTitle("Create flight")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QVBoxLayout()

        self.task_selector = QFlightTypeComboBox(
            self.game.theater, package.target
        )
        self.task_selector.setCurrentIndex(0)
        self.task_selector.currentTextChanged.connect(
            self.on_task_changed)
        layout.addLayout(QLabeledWidget("Task:", self.task_selector))

        self.aircraft_selector = QAircraftTypeSelector(
            self.game.aircraft_inventory.available_types_for_player, self.game.player_country, self.task_selector.currentData()
        )
        self.aircraft_selector.setCurrentIndex(0)
        self.aircraft_selector.currentIndexChanged.connect(
            self.on_aircraft_changed)
        layout.addLayout(QLabeledWidget("Aircraft:", self.aircraft_selector))

        self.departure = QOriginAirfieldSelector(
            self.game.aircraft_inventory,
            [cp for cp in game.theater.controlpoints if cp.captured],
            self.aircraft_selector.currentData()
        )
        self.departure.availability_changed.connect(self.update_max_size)
        layout.addLayout(QLabeledWidget("Departure:", self.departure))

        self.arrival = QArrivalAirfieldSelector(
            [cp for cp in game.theater.controlpoints if cp.captured],
            self.aircraft_selector.currentData(),
            "Same as departure"
        )
        layout.addLayout(QLabeledWidget("Arrival:", self.arrival))

        self.divert = QArrivalAirfieldSelector(
            [cp for cp in game.theater.controlpoints if cp.captured],
            self.aircraft_selector.currentData(),
            "None"
        )
        layout.addLayout(QLabeledWidget("Divert:", self.divert))

        self.flight_size_spinner = QFlightSizeSpinner()
        self.update_max_size(self.departure.available)
        layout.addLayout(QLabeledWidget("Size:", self.flight_size_spinner))

        self.client_slots_spinner = QFlightSizeSpinner(
            min_size=0,
            max_size=self.flight_size_spinner.value(),
            default_size=0
        )
        self.flight_size_spinner.valueChanged.connect(
            lambda v: self.client_slots_spinner.setMaximum(v)
        )
        layout.addLayout(
            QLabeledWidget("Client Slots:", self.client_slots_spinner))

        self.custom_name = QLineEdit()
        self.custom_name.textChanged.connect(self.set_custom_name_text)
        layout.addLayout(
            QLabeledWidget("Custom Flight Name (Optional)", self.custom_name)
        )

        layout.addStretch()

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_flight)
        layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def set_custom_name_text(self, text: str):
        self.custom_name_text = text

    def verify_form(self) -> Optional[str]:
        aircraft: PlaneType = self.aircraft_selector.currentData()
        origin: ControlPoint = self.departure.currentData()
        arrival: ControlPoint = self.arrival.currentData()
        divert: ControlPoint = self.divert.currentData()
        size: int = self.flight_size_spinner.value()
        if aircraft == None:
            return "You must select an aircraft type."
        if not origin.captured:
            return f"{origin.name} is not owned by your coalition."
        if arrival is not None and not arrival.captured:
            return f"{arrival.name} is not owned by your coalition."
        if divert is not None and not divert.captured:
            return f"{divert.name} is not owned by your coalition."
        available = origin.base.aircraft.get(aircraft, 0)
        if not available:
            return f"{origin.name} has no {aircraft.id} available."
        if size > available:
            return f"{origin.name} has only {available} {aircraft.id} available."
        if size <= 0:
            return f"Flight must have at least one aircraft."
        if self.custom_name_text and "|" in self.custom_name_text:
            return f"Cannot include | in flight name"
        return None

    def create_flight(self) -> None:
        error = self.verify_form()
        if error is not None:
            QMessageBox.critical(self, "Could not create flight", error,
                                 QMessageBox.Ok)
            return

        task = self.task_selector.currentData()
        aircraft = self.aircraft_selector.currentData()
        origin = self.departure.currentData()
        arrival = self.arrival.currentData()
        divert = self.divert.currentData()
        size = self.flight_size_spinner.value()

        if arrival is None:
            arrival = origin

        if isinstance(origin, OffMapSpawn):
            start_type = "In Flight"
        elif self.game.settings.perf_ai_parking_start:
            start_type = "Cold"
        else:
            start_type = "Warm"
        flight = Flight(self.package, self.country, aircraft, size, task, start_type, origin,
                        arrival, divert, custom_name=self.custom_name_text)
        flight.client_count = self.client_slots_spinner.value()

        # noinspection PyUnresolvedReferences
        self.created.emit(flight)
        self.close()

    def on_aircraft_changed(self, index: int) -> None:
        new_aircraft = self.aircraft_selector.itemData(index)
        self.departure.change_aircraft(new_aircraft)
        self.arrival.change_aircraft(new_aircraft)
        self.divert.change_aircraft(new_aircraft)

    def on_task_changed(self) -> None:
        self.aircraft_selector.updateItems(self.task_selector.currentData(), self.game.aircraft_inventory.available_types_for_player)

    def update_max_size(self, available: int) -> None:
        self.flight_size_spinner.setMaximum(min(available, 4))
        if self.flight_size_spinner.maximum() >= 2:
            if self.flight_size_spinner.value() < 2:
                self.flight_size_spinner.setValue(2)
