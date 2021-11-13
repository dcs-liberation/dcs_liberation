from PySide2.QtWidgets import QTabWidget

from game import Game
from game.ato.flight import Flight
from qt_ui.models import PackageModel
from qt_ui.windows.mission.flight.payload.QFlightPayloadTab import QFlightPayloadTab
from qt_ui.windows.mission.flight.settings.QGeneralFlightSettingsTab import (
    QGeneralFlightSettingsTab,
)
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointTab import QFlightWaypointTab


class QFlightPlanner(QTabWidget):
    def __init__(self, package_model: PackageModel, flight: Flight, game: Game):
        super().__init__()

        self.general_settings_tab = QGeneralFlightSettingsTab(
            game, package_model, flight
        )
        self.payload_tab = QFlightPayloadTab(flight, game)
        self.waypoint_tab = QFlightWaypointTab(game, package_model.package, flight)
        self.waypoint_tab.loadout_changed.connect(self.payload_tab.reload_from_flight)
        self.addTab(self.general_settings_tab, "General Flight settings")
        self.addTab(self.payload_tab, "Payload")
        self.addTab(self.waypoint_tab, "Waypoints")
        self.setCurrentIndex(0)
