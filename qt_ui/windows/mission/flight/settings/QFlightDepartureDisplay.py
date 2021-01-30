from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QVBoxLayout

from gen.flights.flight import Flight
from gen.flights.traveltime import TotEstimator


from qt_ui.models import PackageModel


class QFlightDepartureDisplay(QGroupBox):

    def __init__(self, package_model: PackageModel, flight: Flight):
        super().__init__("Departure")
        self.package_model = package_model
        self.flight = flight

        layout = QVBoxLayout()

        departure_row = QHBoxLayout()
        layout.addLayout(departure_row)

        departure_row.addWidget(QLabel(
            f"Departing from <b>{flight.from_cp.name}</b>"
        ))
        self.departure_time = QLabel()
        self.package_model.tot_changed.connect(self.update_departure_time)
        departure_row.addWidget(self.departure_time)
        self.update_departure_time()

        layout.addWidget(QLabel("Determined based on the package TOT. Edit the "
                                "package to adjust the TOT."))

        self.setLayout(layout)

    def update_departure_time(self) -> None:
        estimator = TotEstimator(self.package_model.package)
        delay = estimator.mission_start_time(self.flight)
        self.departure_time.setText(f"At T+{delay}")
