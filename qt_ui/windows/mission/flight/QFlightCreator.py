from typing import Optional, Type

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
)
from dcs.unittype import FlyingType

from game import Game
from game.ato.starttype import StartType
from game.squadrons.squadron import Squadron
from game.theater import ControlPoint, OffMapSpawn
from game.ato.package import Package
from game.ato.flightroster import FlightRoster
from game.ato.flight import Flight
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QFlightSizeSpinner import QFlightSizeSpinner
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.combos.QAircraftTypeSelector import QAircraftTypeSelector
from qt_ui.widgets.combos.QArrivalAirfieldSelector import QArrivalAirfieldSelector
from qt_ui.widgets.combos.QFlightTypeComboBox import QFlightTypeComboBox
from qt_ui.windows.mission.flight.SquadronSelector import SquadronSelector
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import FlightRosterEditor


class QFlightCreator(QDialog):
    created = Signal(Flight)

    def __init__(self, game: Game, package: Package, parent=None) -> None:
        super().__init__(parent=parent)
        self.setMinimumWidth(400)

        self.game = game
        self.package = package
        self.custom_name_text = None
        self.country = self.game.blue.country_name

        # Make dialog modal to prevent background windows to close unexpectedly.
        self.setModal(True)

        self.setWindowTitle("Create flight")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QVBoxLayout()

        self.task_selector = QFlightTypeComboBox(
            self.game.theater, package.target, self.game.settings
        )
        self.task_selector.setCurrentIndex(0)
        self.task_selector.currentIndexChanged.connect(self.on_task_changed)
        layout.addLayout(QLabeledWidget("Task:", self.task_selector))

        self.aircraft_selector = QAircraftTypeSelector(
            self.game.blue.air_wing.best_available_aircrafts_for(
                self.task_selector.currentData()
            )
        )
        self.aircraft_selector.setCurrentIndex(0)
        self.aircraft_selector.currentIndexChanged.connect(self.on_aircraft_changed)
        layout.addLayout(QLabeledWidget("Aircraft:", self.aircraft_selector))

        self.squadron_selector = SquadronSelector(
            self.game.air_wing_for(player=True),
            self.task_selector.currentData(),
            self.aircraft_selector.currentData(),
        )
        self.squadron_selector.setCurrentIndex(0)
        layout.addLayout(QLabeledWidget("Squadron:", self.squadron_selector))

        self.divert = QArrivalAirfieldSelector(
            [cp for cp in game.theater.controlpoints if cp.captured],
            self.aircraft_selector.currentData(),
            "None",
        )
        layout.addLayout(QLabeledWidget("Divert:", self.divert))

        self.flight_size_spinner = QFlightSizeSpinner()
        self.update_max_size(self.squadron_selector.aircraft_available)
        layout.addLayout(QLabeledWidget("Size:", self.flight_size_spinner))

        squadron = self.squadron_selector.currentData()
        if squadron is None:
            roster = None
        else:
            roster = FlightRoster(
                squadron, initial_size=self.flight_size_spinner.value()
            )
        self.roster_editor = FlightRosterEditor(roster)
        self.flight_size_spinner.valueChanged.connect(self.roster_editor.resize)
        self.squadron_selector.currentIndexChanged.connect(self.on_squadron_changed)
        roster_layout = QHBoxLayout()
        layout.addLayout(roster_layout)
        roster_layout.addWidget(QLabel("Assigned pilots:"))
        roster_layout.addLayout(self.roster_editor)

        # When an off-map spawn overrides the start type to in-flight, we save
        # the selected type into this value. If a non-off-map spawn is selected
        # we restore the previous choice.
        self.restore_start_type = self.game.settings.default_start_type
        self.start_type = QComboBox()
        for start_type in StartType:
            self.start_type.addItem(start_type.value, start_type)
        self.start_type.setCurrentText(self.game.settings.default_start_type.value)
        layout.addLayout(
            QLabeledWidget(
                "Start type:",
                self.start_type,
                tooltip="Selects the start type for this flight.",
            )
        )
        if squadron is not None and isinstance(squadron.location, OffMapSpawn):
            self.start_type.setCurrentText(StartType.IN_FLIGHT.value)
            self.start_type.setEnabled(False)
        layout.addWidget(
            QLabel(
                "Any option other than Cold will make this flight "
                + "non-targetable<br />by OCA/Aircraft missions. This will affect "
                + "game balance."
            )
        )

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

    def reject(self) -> None:
        super().reject()
        # Clear the roster to return pilots to the pool.
        self.roster_editor.replace(None)

    def set_custom_name_text(self, text: str):
        self.custom_name_text = text

    def verify_form(self) -> Optional[str]:
        aircraft: Optional[Type[FlyingType]] = self.aircraft_selector.currentData()
        squadron: Optional[Squadron] = self.squadron_selector.currentData()
        divert: Optional[ControlPoint] = self.divert.currentData()
        size: int = self.flight_size_spinner.value()
        if aircraft is None:
            return "You must select an aircraft type."
        if squadron is None:
            return "You must select a squadron."
        if divert is not None and not divert.captured:
            return f"{divert.name} is not owned by your coalition."
        available = squadron.untasked_aircraft
        if not available:
            return f"{squadron} has no aircraft available."
        if size > available:
            return f"{squadron} has only {available} aircraft available."
        if size <= 0:
            return f"Flight must have at least one aircraft."
        if self.custom_name_text and "|" in self.custom_name_text:
            return f"Cannot include | in flight name"
        return None

    def create_flight(self) -> None:
        error = self.verify_form()
        if error is not None:
            QMessageBox.critical(self, "Could not create flight", error, QMessageBox.Ok)
            return

        task = self.task_selector.currentData()
        squadron = self.squadron_selector.currentData()
        divert = self.divert.currentData()
        roster = self.roster_editor.roster

        flight = Flight(
            self.package,
            self.country,
            squadron,
            # A bit of a hack to work around the old API. Not actually relevant because
            # the roster is passed explicitly. Needs a refactor.
            roster.max_size,
            task,
            self.start_type.currentData(),
            divert,
            custom_name=self.custom_name_text,
            roster=roster,
        )

        # noinspection PyUnresolvedReferences
        self.created.emit(flight)
        self.accept()

    def on_aircraft_changed(self, index: int) -> None:
        new_aircraft = self.aircraft_selector.itemData(index)
        self.squadron_selector.update_items(
            self.task_selector.currentData(), new_aircraft
        )
        self.divert.change_aircraft(new_aircraft)

    def on_departure_changed(self, departure: ControlPoint) -> None:
        if isinstance(departure, OffMapSpawn):
            previous_type = self.start_type.currentData()
            if previous_type != StartType.IN_FLIGHT:
                self.restore_start_type = previous_type
            self.start_type.setCurrentText(StartType.IN_FLIGHT.value)
            self.start_type.setEnabled(False)
        else:
            self.start_type.setEnabled(True)
            if self.restore_start_type is not None:
                self.start_type.setCurrentText(self.restore_start_type.value)
                self.restore_start_type = None

    def on_task_changed(self, index: int) -> None:
        task = self.task_selector.itemData(index)
        self.aircraft_selector.update_items(
            self.game.blue.air_wing.best_available_aircrafts_for(task)
        )
        self.squadron_selector.update_items(task, self.aircraft_selector.currentData())

    def on_squadron_changed(self, index: int) -> None:
        squadron: Optional[Squadron] = self.squadron_selector.itemData(index)
        self.update_max_size(self.squadron_selector.aircraft_available)
        # Clear the roster first so we return the pilots to the pool. This way if we end
        # up repopulating from the same squadron we'll get the same pilots back.
        self.roster_editor.replace(None)
        if squadron is not None:
            self.roster_editor.replace(
                FlightRoster(squadron, self.flight_size_spinner.value())
            )
            self.on_departure_changed(squadron.location)

    def update_max_size(self, available: int) -> None:
        aircraft = self.aircraft_selector.currentData()
        if aircraft is None:
            self.flight_size_spinner.setMaximum(0)
            return

        self.flight_size_spinner.setMaximum(min(available, aircraft.max_group_size))

        default_size = max(2, available, aircraft.max_group_size)
        self.flight_size_spinner.setValue(default_size)
