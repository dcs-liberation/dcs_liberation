from PySide2.QtGui import QStandardItem, QIcon

from game import db
from gen.flights.flight import Flight
from qt_ui.uiconstants import AIRCRAFT_ICONS


class QFlightItem(QStandardItem):

    def __init__(self, flight:Flight):
        super(QFlightItem, self).__init__()
        self.flight = flight

        if db.unit_type_name(self.flight.unit_type).replace("/", " ") in AIRCRAFT_ICONS.keys():
            icon = QIcon((AIRCRAFT_ICONS[db.unit_type_name(self.flight.unit_type)]))
            self.setIcon(icon)
        self.setEditable(False)
        self.setText("["+str(self.flight.flight_type.name[:6])+"] "
                     + str(self.flight.count) + " x " + db.unit_type_name(self.flight.unit_type)
                     + "   in " + str(self.flight.scheduled_in) + " minutes")

    def update(self, flight):
        self.flight = flight
        self.setText("[" + str(self.flight.flight_type.name[:6]) + "] "
                     + str(self.flight.count) + " x " + db.unit_type_name(self.flight.unit_type)
                     + "   in " + str(self.flight.scheduled_in) + " minutes")