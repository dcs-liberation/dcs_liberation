import datetime

from PySide2.QtGui import QStandardItem, QIcon

from game import db
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

        if db.unit_type_name(self.flight.unit_type).replace("/", " ") in AIRCRAFT_ICONS.keys():
            icon = QIcon((AIRCRAFT_ICONS[db.unit_type_name(self.flight.unit_type)]))
            self.setIcon(icon)
        self.setEditable(False)
        estimator = TotEstimator(self.package)
        delay = estimator.mission_start_time(flight)
        self.setText("["+str(self.flight.flight_type.name[:6])+"] "
                     + str(self.flight.count) + " x " + db.unit_type_name(self.flight.unit_type)
                     + "   in " + str(delay))
