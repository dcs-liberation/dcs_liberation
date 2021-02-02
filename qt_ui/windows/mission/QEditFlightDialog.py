"""Dialog window for editing flights."""
from PySide2.QtWidgets import (
    QDialog,
    QVBoxLayout,
)

from gen.flights.flight import Flight
from qt_ui.models import GameModel, PackageModel
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.mission.flight.QFlightPlanner import QFlightPlanner


class QEditFlightDialog(QDialog):
    """Dialog window for editing flight plans and loadouts."""

    def __init__(self, game_model: GameModel, package_model: PackageModel,
                 flight: Flight, parent=None) -> None:
        super().__init__(parent=parent)

        self.game_model = game_model

        self.setWindowTitle("Edit flight")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QVBoxLayout()

        self.flight_planner = QFlightPlanner(package_model, flight,
                                             game_model.game)
        layout.addWidget(self.flight_planner)

        self.setLayout(layout)
        self.finished.connect(self.on_close)

    def on_close(self, _result) -> None:
        GameUpdateSignal.get_instance().redraw_flight_paths()
        self.game_model.ato_model.client_slots_changed.emit()
