import logging

from PySide2.QtWidgets import QGroupBox, QLabel, QMessageBox, QVBoxLayout

from game import Game
from game.ato.flight import Flight
from game.ato.flightplans.planningerror import PlanningError
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

        arrival_label = QLabel(f"<b>{flight.arrival.name}</b>")
        layout.addLayout(QLabeledWidget("Arrival:", arrival_label))

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
        if not self.flight.package.flights:
            # This is theoretically impossible, but for some reason the dialog that owns
            # this object QEditFlightDialog does not dispose properly on close, so this
            # handler may be called for a flight whose package has been canceled, which
            # is an invalid state for calling anything in TotEstimator.
            return
        self.departure_time.setText(f"At T+{self.flight.flight_plan.startup_time()}")

    def set_divert(self, index: int) -> None:
        old_divert = self.flight.divert
        divert = self.divert.itemData(index)
        if divert == old_divert:
            return

        self.flight.divert = divert
        try:
            self.flight.recreate_flight_plan()
        except PlanningError as ex:
            self.flight.divert = old_divert
            logging.exception("Could not change divert airfield")
            QMessageBox.critical(
                self, "Could not update flight plan", str(ex), QMessageBox.Ok
            )
