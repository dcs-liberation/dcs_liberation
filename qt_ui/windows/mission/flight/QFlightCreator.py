import logging
from typing import Optional

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
)
from dcs.planes import PlaneType

from game import Game
from gen.ato import Package
from gen.flights.ai_flight_planner import FlightPlanner
from gen.flights.flight import Flight, FlightType
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.QFlightSizeSpinner import QFlightSizeSpinner
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.combos.QAircraftTypeSelector import QAircraftTypeSelector
from qt_ui.widgets.combos.QFlightTypeComboBox import QFlightTypeComboBox
from qt_ui.widgets.combos.QOriginAirfieldSelector import QOriginAirfieldSelector
from theater import ControlPoint, FrontLine, TheaterGroundObject


class QFlightCreator(QDialog):
    created = Signal(Flight)

    def __init__(self, game: Game, package: Package) -> None:
        super().__init__()

        self.game = game
        self.package = package

        self.setWindowTitle("Create flight")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QVBoxLayout()

        self.task_selector = QFlightTypeComboBox(
            self.game.theater, self.package.target
        )
        self.task_selector.setCurrentIndex(0)
        layout.addLayout(QLabeledWidget("Task:", self.task_selector))

        self.aircraft_selector = QAircraftTypeSelector(
            self.game.aircraft_inventory.available_types_for_player
        )
        self.aircraft_selector.setCurrentIndex(0)
        self.aircraft_selector.currentIndexChanged.connect(
            self.on_aircraft_changed)
        layout.addLayout(QLabeledWidget("Aircraft:", self.aircraft_selector))

        self.airfield_selector = QOriginAirfieldSelector(
            self.game.aircraft_inventory,
            [cp for cp in game.theater.controlpoints if cp.captured],
            self.aircraft_selector.currentData()
        )
        layout.addLayout(QLabeledWidget("Airfield:", self.airfield_selector))

        self.flight_size_spinner = QFlightSizeSpinner()
        layout.addLayout(QLabeledWidget("Count:", self.flight_size_spinner))

        layout.addStretch()

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_flight)
        layout.addWidget(self.create_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def verify_form(self) -> Optional[str]:
        aircraft: PlaneType = self.aircraft_selector.currentData()
        origin: ControlPoint = self.airfield_selector.currentData()
        size: int = self.flight_size_spinner.value()
        if not origin.captured:
            return f"{origin.name} is not owned by your coalition."
        available = origin.base.aircraft.get(aircraft, 0)
        if not available:
            return f"{origin.name} has no {aircraft.id} available."
        if size > available:
            return f"{origin.name} has only {available} {aircraft.id} available."
        return None

    def create_flight(self) -> None:
        error = self.verify_form()
        if error is not None:
            self.error_box("Could not create flight", error)
            return

        task = self.task_selector.currentData()
        aircraft = self.aircraft_selector.currentData()
        origin = self.airfield_selector.currentData()
        size = self.flight_size_spinner.value()

        flight = Flight(aircraft, size, origin, task)
        self.populate_flight_plan(flight, task)

        # noinspection PyUnresolvedReferences
        self.created.emit(flight)
        self.close()

    def on_aircraft_changed(self, index: int) -> None:
        new_aircraft = self.aircraft_selector.itemData(index)
        self.airfield_selector.change_aircraft(new_aircraft)

    @property
    def planner(self) -> FlightPlanner:
        return self.game.planners[self.airfield_selector.currentData().id]

    def populate_flight_plan(self, flight: Flight, task: FlightType) -> None:
        # TODO: Flesh out mission types.
        if task == FlightType.ANTISHIP:
            logging.error("Anti-ship flight plan generation not implemented")
        elif task == FlightType.BAI:
            logging.error("BAI flight plan generation not implemented")
        elif task == FlightType.BARCAP:
            self.generate_cap(flight)
        elif task == FlightType.CAP:
            self.generate_cap(flight)
        elif task == FlightType.CAS:
            self.generate_cas(flight)
        elif task == FlightType.DEAD:
            self.generate_sead(flight)
        elif task == FlightType.ELINT:
            logging.error("ELINT flight plan generation not implemented")
        elif task == FlightType.EVAC:
            logging.error("Evac flight plan generation not implemented")
        elif task == FlightType.EWAR:
            logging.error("EWar flight plan generation not implemented")
        elif task == FlightType.INTERCEPTION:
            logging.error("Intercept flight plan generation not implemented")
        elif task == FlightType.LOGISTICS:
            logging.error("Logistics flight plan generation not implemented")
        elif task == FlightType.RECON:
            logging.error("Recon flight plan generation not implemented")
        elif task == FlightType.SEAD:
            self.generate_sead(flight)
        elif task == FlightType.STRIKE:
            self.generate_strike(flight)
        elif task == FlightType.TARCAP:
            self.generate_cap(flight)
        elif task == FlightType.TROOP_TRANSPORT:
            logging.error(
                "Troop transport flight plan generation not implemented"
            )

    def generate_cas(self, flight: Flight) -> None:
        if not isinstance(self.package.target, FrontLine):
            logging.error(
                "Could not create flight plan: CAS missions only valid for "
                "front lines"
            )
            return
        self.planner.generate_cas(flight, self.package.target)

    def generate_cap(self, flight: Flight) -> None:
        if isinstance(self.package.target, TheaterGroundObject):
            logging.error(
                "Could not create flight plan: CAP missions for strike targets "
                "not implemented"
            )
            return
        if isinstance(self.package.target, FrontLine):
            self.planner.generate_frontline_cap(flight, self.package.target)
        else:
            self.planner.generate_barcap(flight, self.package.target)

    def generate_sead(self, flight: Flight) -> None:
        self.planner.generate_sead(flight, self.package.target)

    def generate_strike(self, flight: Flight) -> None:
        if not isinstance(self.package.target, TheaterGroundObject):
            logging.error(
                "Could not create flight plan: strike missions for capture "
                "points not implemented"
            )
            return
        self.planner.generate_strike(flight, self.package.target)
