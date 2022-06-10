import logging

from PySide2.QtWidgets import QGroupBox, QLabel, QMessageBox, QVBoxLayout

from game import Game
from game.ato.flight import Flight
from game.ato.flightplans.flightplanbuilder import FlightPlanBuilder
from game.ato.flightplans.planningerror import PlanningError
from game.ato.traveltime import TotEstimator
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

        layout.addLayout(QLabeledWidget("Arrival:", QLabel(f"<b>{flight.arrival.name}</b>")))

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
