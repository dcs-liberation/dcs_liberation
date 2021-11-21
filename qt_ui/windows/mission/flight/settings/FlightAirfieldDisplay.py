import logging

from PySide6.QtWidgets import QGroupBox, QLabel, QMessageBox, QVBoxLayout

from game import Game
from game.ato.flight import Flight
from gen.flights.flightplan import FlightPlanBuilder, PlanningError
from gen.flights.traveltime import TotEstimator
from qt_ui.models import PackageModel
from qt_ui.widgets.QLabeledWidget import QLabeledWidget
from qt_ui.widgets.combos.QArrivalAirfieldSelector import QArrivalAirfieldSelector


class FlightAirfieldDisplay(QGroupBox):
    def __init__(self, game: Game, package_model: PackageModel, flight: Flight) -> None:
        super().__init__("Departure/Arrival")
        self.game = game
        self.package_model = package_model
        self.flight = flight

        layout = QVBoxLayout()

        self.departure_time = QLabel()
        layout.addLayout(
            QLabeledWidget(
                f"Departing from <b>{flight.from_cp.name}</b>", self.departure_time
            )
        )
        self.package_model.tot_changed.connect(self.update_departure_time)
        self.update_departure_time()

        layout.addWidget(
            QLabel(
                "Determined based on the package TOT. Edit the "
                "package to adjust the TOT."
            )
        )

        self.arrival = QArrivalAirfieldSelector(
            [cp for cp in game.theater.controlpoints if cp.captured],
            flight.unit_type,
            "Same as departure",
        )
        self.arrival.currentIndexChanged.connect(self.set_arrival)
        if flight.arrival != flight.departure:
            self.arrival.setCurrentText(flight.arrival.name)
        layout.addLayout(QLabeledWidget("Arrival:", self.arrival))

        self.divert = QArrivalAirfieldSelector(
            [cp for cp in game.theater.controlpoints if cp.captured],
            flight.unit_type,
            "None",
        )
        self.divert.currentIndexChanged.connect(self.set_divert)
        if flight.divert is not None:
            self.divert.setCurrentText(flight.divert.name)
        layout.addLayout(QLabeledWidget("Divert:", self.divert))

        self.setLayout(layout)

    def update_departure_time(self) -> None:
        estimator = TotEstimator(self.package_model.package)
        delay = estimator.mission_start_time(self.flight)
        self.departure_time.setText(f"At T+{delay}")

    def set_arrival(self, index: int) -> None:
        old_arrival = self.flight.arrival
        arrival = self.arrival.itemData(index)
        if arrival == old_arrival:
            return

        if arrival is None:
            arrival = self.flight.departure

        self.flight.arrival = arrival
        try:
            self.update_flight_plan()
        except PlanningError as ex:
            self.flight.arrival = old_arrival
            logging.exception("Could not change arrival airfield")
            QMessageBox.critical(
                self, "Could not update flight plan", str(ex), QMessageBox.Ok
            )

    def set_divert(self, index: int) -> None:
        old_divert = self.flight.divert
        divert = self.divert.itemData(index)
        if divert == old_divert:
            return

        self.flight.divert = divert
        try:
            self.update_flight_plan()
        except PlanningError as ex:
            self.flight.divert = old_divert
            logging.exception("Could not change divert airfield")
            QMessageBox.critical(
                self, "Could not update flight plan", str(ex), QMessageBox.Ok
            )

    def update_flight_plan(self) -> None:
        planner = FlightPlanBuilder(
            self.package_model.package, self.game.blue, self.game.theater
        )
        planner.populate_flight_plan(self.flight)
