from PySide2.QtGui import QIcon, QStandardItem

from game.ato.package import Package
from game.ato.scheduledflight import ScheduledFlight
from game.ato.traveltime import TotEstimator
from qt_ui.uiconstants import AIRCRAFT_ICONS


# TODO: Replace with QFlightList.
class QFlightItem(QStandardItem):
    def __init__(self, package: Package, flight: ScheduledFlight):
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
