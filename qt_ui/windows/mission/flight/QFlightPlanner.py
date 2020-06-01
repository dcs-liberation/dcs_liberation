from PySide2.QtWidgets import QTabWidget, QFrame, QGridLayout, QLabel

from gen.flights.flight import Flight
from game import Game
from qt_ui.windows.mission.flight.payload.QFlightPayloadTab import QFlightPayloadTab
from qt_ui.windows.mission.flight.settings.QGeneralFlightSettingsTab import QGeneralFlightSettingsTab
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointTab import QFlightWaypointTab


class QFlightPlanner(QTabWidget):

    def __init__(self, flight: Flight, game: Game, planner):
        super(QFlightPlanner, self).__init__()
        self.tabCount = 0
        if flight:
            self.general_settings_tab = QGeneralFlightSettingsTab(flight, game, planner)
            self.payload_tab = QFlightPayloadTab(flight, game)
            self.waypoint_tab = QFlightWaypointTab(game, flight)
            self.addTab(self.general_settings_tab, "General Flight settings")
            self.addTab(self.payload_tab, "Payload")
            self.addTab(self.waypoint_tab, "Waypoints")
            self.tabCount = 3
        else:
            tabError = QFrame()
            l = QGridLayout()
            l.addWidget(QLabel("No flight selected"))
            tabError.setLayout(l)
            self.addTab(tabError, "No flight")
            self.tabCount = 1

    def clearTabs(self):
        for i in range(self.tabCount):
            self.removeTab(i)