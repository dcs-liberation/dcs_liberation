from PySide2.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout

from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import QFlightWaypointList
from qt_ui.windows.mission.flight.waypoints.QWaypointSelectionWindow import QWaypointSelectionWindow
from game import Game

class QFlightWaypointTab(QFrame):

    def __init__(self, game: Game, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.flight = flight
        self.game = game
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        rlayout = QVBoxLayout()
        self.flight_waypoint_list = QFlightWaypointList(self.flight)
        self.open_fast_waypoint_button = QPushButton("Add Waypoint")
        self.open_fast_waypoint_button.clicked.connect(self.on_fast_waypoint)
        self.delete_selected = QPushButton("Delete Selected")
        self.delete_selected.clicked.connect(self.on_delete_waypoint)


        layout.addWidget(self.flight_waypoint_list,0,0)
        rlayout.addWidget(self.open_fast_waypoint_button)
        rlayout.addWidget(self.delete_selected)
        rlayout.addStretch()
        layout.addLayout(rlayout, 0, 1)
        self.setLayout(layout)

    def on_delete_waypoint(self):
        wpt = self.flight_waypoint_list.selectionModel().currentIndex().row()
        if wpt > 0:
            del self.flight.points[wpt-1]
            self.flight_waypoint_list.update_list()

    def on_fast_waypoint(self):
        self.subwindow = QWaypointSelectionWindow(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.show()