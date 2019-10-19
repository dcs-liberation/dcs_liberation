from PySide2.QtWidgets import QFrame, QGridLayout, QLabel

from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import QFlightWaypointList


class QFlightWaypointTab(QFrame):

    def __init__(self, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.flight = flight
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        self.flight_waypoint_list = QFlightWaypointList(self.flight)
        layout.addWidget(self.flight_waypoint_list)
        self.setLayout(layout)
