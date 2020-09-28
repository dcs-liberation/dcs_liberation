"""Dialog window for editing flights."""
from PySide2.QtWidgets import (
    QDialog,
    QVBoxLayout,
)

from game import Game
from gen.flights.flight import Flight
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.mission.flight.QFlightPlanner import QFlightPlanner


class QEditFlightDialog(QDialog):
    """Dialog window for editing flight plans and loadouts."""

    def __init__(self, game: Game, flight: Flight) -> None:
        super().__init__()

        self.game = game

        self.setWindowTitle("Create flight")
        self.setWindowIcon(EVENT_ICONS["strike"])

        layout = QVBoxLayout()

        self.flight_planner = QFlightPlanner(flight, game)
        layout.addWidget(self.flight_planner)

        self.setLayout(layout)
        self.finished.connect(self.on_close)

    @staticmethod
    def on_close(_result) -> None:
        GameUpdateSignal.get_instance().redraw_flight_paths()
