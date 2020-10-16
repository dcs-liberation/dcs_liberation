import datetime

from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QVBoxLayout

from gen.ato import Package
from gen.flights.flight import Flight
from gen.flights.traveltime import TotEstimator


# TODO: Remove?
class QFlightDepartureDisplay(QGroupBox):

    def __init__(self, package: Package, flight: Flight):
        super().__init__("Departure")

        layout = QVBoxLayout()

        departure_row = QHBoxLayout()
        layout.addLayout(departure_row)

        estimator = TotEstimator(package)
        delay = datetime.timedelta(seconds=estimator.mission_start_time(flight))

        departure_row.addWidget(QLabel(
            f"Departing from <b>{flight.from_cp.name}</b>"
        ))
        departure_row.addWidget(QLabel(f"At T+{delay}"))

        layout.addWidget(QLabel("Determined based on the package TOT. Edit the "
                                "package to adjust the TOT."))

        self.setLayout(layout)
