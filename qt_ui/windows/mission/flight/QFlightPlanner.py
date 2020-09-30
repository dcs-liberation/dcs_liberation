from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget

from game import Game
from gen.ato import Package
from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.payload.QFlightPayloadTab import \
    QFlightPayloadTab
from qt_ui.windows.mission.flight.settings.QGeneralFlightSettingsTab import \
    QGeneralFlightSettingsTab
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointTab import \
    QFlightWaypointTab


class QFlightPlanner(QTabWidget):

    on_planned_flight_changed = Signal()

    def __init__(self, package: Package, flight: Flight, game: Game):
        super().__init__()

        self.general_settings_tab = QGeneralFlightSettingsTab(game, flight)
        self.general_settings_tab.on_flight_settings_changed.connect(
            lambda: self.on_planned_flight_changed.emit())
        self.payload_tab = QFlightPayloadTab(flight, game)
        self.waypoint_tab = QFlightWaypointTab(game, package, flight)
        self.waypoint_tab.on_flight_changed.connect(
            lambda: self.on_planned_flight_changed.emit())
        self.addTab(self.general_settings_tab, "General Flight settings")
        self.addTab(self.payload_tab, "Payload")
        self.addTab(self.waypoint_tab, "Waypoints")
        self.setCurrentIndex(0)
