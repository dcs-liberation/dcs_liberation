from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QPushButton

from game import Game
from gen.flights.flight import Flight
from gen.flights.flightplan import FlightPlanBuilder
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointInfoBox import QFlightWaypointInfoBox


class QAbstractMissionGenerator(QDialog):

    def __init__(self, game: Game, flight: Flight, flight_waypoint_list, title):
        super(QAbstractMissionGenerator, self).__init__()
        self.game = game
        self.flight = flight
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(400, 250)
        self.setModal(True)
        self.setWindowTitle(title)
        self.setWindowIcon(EVENT_ICONS["strike"])
        self.flight_waypoint_list = flight_waypoint_list
        self.planner = FlightPlanBuilder(self.game, is_player=True)

        self.selected_waypoints = []
        self.wpt_info = QFlightWaypointInfoBox()

        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.apply)

    def on_select_wpt_changed(self):
        self.selected_waypoints = self.wpt_selection_box.get_selected_waypoints(False)
        if self.selected_waypoints is None or len(self.selected_waypoints) <= 0:
            self.ok_button.setDisabled(True)
        else:
            self.wpt_info.set_flight_waypoint(self.selected_waypoints[0])
            self.ok_button.setDisabled(False)

    def apply(self):
        raise NotImplementedError()




