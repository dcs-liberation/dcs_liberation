from PySide2.QtGui import QStandardItem, QIcon

from gen.ato import Package
from gen.flights.flight import Flight
from gen.flights.traveltime import TotEstimator
from qt_ui.uiconstants import AIRCRAFT_ICONS


# TODO: Replace with QFlightList.
class QFlightItem(QStandardItem):
    def __init__(self, package: Package, flight: Flight):
        super(QFlightItem, self).__init__()
        self.package = package
        self.flight = flight

        if self.flight.unit_type.dcs_id in AIRCRAFT_ICONS:
            icon = QIcon((AIRCRAFT_ICONS[self.flight.unit_type.dcs_id]))
            self.setIcon(icon)
        self.setEditable(False)
        estimator = TotEstimator(self.package)
        delay = estimator.mission_start_time(flight)
        self.setText(f"{flight} in {delay}")
