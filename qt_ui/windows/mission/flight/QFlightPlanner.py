from PySide2.QtWidgets import QTabWidget

from gen.flights.flight import Flight
from game import Game
from qt_ui.windows.mission.flight.payload.QFlightPayloadTab import QFlightPayloadTab
from qt_ui.windows.mission.flight.settings.QGeneralFlightSettingsTab import QGeneralFlightSettingsTab
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointTab import QFlightWaypointTab


class QFlightPlanner(QTabWidget):

    def __init__(self, flight: Flight, game: Game):
        super(QFlightPlanner, self).__init__()
        self.general_settings_tab = QGeneralFlightSettingsTab(flight, game)
        self.payload_tab = QFlightPayloadTab(flight)
        self.waypoint_tab = QFlightWaypointTab(flight)
        self.addTab(self.general_settings_tab, "General Flight settings")
        self.addTab(self.payload_tab, "Payload")
        self.addTab(self.waypoint_tab, "Waypoints")