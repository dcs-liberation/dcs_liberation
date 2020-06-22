from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget, QFrame, QGridLayout, QLabel

from gen.flights.flight import Flight
from game import Game
from qt_ui.windows.mission.flight.payload.QFlightPayloadTab import QFlightPayloadTab
from qt_ui.windows.mission.flight.settings.QGeneralFlightSettingsTab import QGeneralFlightSettingsTab
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointTab import QFlightWaypointTab


class QFlightPlanner(QTabWidget):

    on_planned_flight_changed = Signal()

    def __init__(self, flight: Flight, game: Game, planner, selected_tab):
        super(QFlightPlanner, self).__init__()

        print(selected_tab)

        self.tabCount = 0
        if flight:
            self.general_settings_tab = QGeneralFlightSettingsTab(flight, game, planner)
            self.general_settings_tab.on_flight_settings_changed.connect(lambda: self.on_planned_flight_changed.emit())
            self.payload_tab = QFlightPayloadTab(flight, game)
            self.waypoint_tab = QFlightWaypointTab(game, flight)
            self.waypoint_tab.on_flight_changed.connect(lambda: self.on_planned_flight_changed.emit())
            self.addTab(self.general_settings_tab, "General Flight settings")
            self.addTab(self.payload_tab, "Payload")
            self.addTab(self.waypoint_tab, "Waypoints")
            self.tabCount = 3
            self.setCurrentIndex(selected_tab)
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
