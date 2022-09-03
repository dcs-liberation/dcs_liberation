from datetime import timedelta

from PySide2.QtCore import QItemSelectionModel, QSize
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QAbstractItemView, QListView

from game.theater.controlpoint import ControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.mission.QFlightItem import QFlightItem


class QPlannedFlightsView(QListView):
    def __init__(self, game_model: GameModel, cp: ControlPoint) -> None:
        super(QPlannedFlightsView, self).__init__()
        self.game_model = game_model
        self.cp = cp
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.flight_items = []
        self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.set_flight_planner()

    def setup_content(self):
        self.flight_items = []
        for package in self.game_model.ato_model.packages:
            for flight in package.flights:
                if flight.from_cp == self.cp:
                    item = QFlightItem(package.package, flight)
                    self.flight_items.append(item)

        self.flight_items.sort(key=self.mission_start_for_flight)
        for item in self.flight_items:
            self.model.appendRow(item)
        self.set_selected_flight(0)

    def set_selected_flight(self, row):
        self.selectionModel().clearSelection()
        index = self.model.index(row, 0)
        if not index.isValid():
            index = self.model.index(0, 0)
        self.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select)
        self.repaint()

    def clear_layout(self):
        self.model.removeRows(0, self.model.rowCount())

    def set_flight_planner(self) -> None:
        self.clear_layout()
        self.setup_content()

    @staticmethod
    def mission_start_for_flight(flight_item: QFlightItem) -> timedelta:
        return flight_item.flight.flight_plan.startup_time()
