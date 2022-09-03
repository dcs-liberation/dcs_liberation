from PySide2.QtGui import QIcon, QStandardItem

from game.ato.flight import Flight
from game.ato.package import Package
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
        self.setText(f"{flight} in {flight.flight_plan.startup_time()}")
