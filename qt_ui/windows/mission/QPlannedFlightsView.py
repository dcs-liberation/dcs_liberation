from PySide2.QtCore import QSize, QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QListView, QAbstractItemView

from gen.flights.ai_flight_planner import FlightPlanner
from qt_ui.windows.mission.QFlightItem import QFlightItem


class QPlannedFlightsView(QListView):

    def __init__(self, flight_planner: FlightPlanner):
        super(QPlannedFlightsView, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.flightitems = []
        self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        if flight_planner:
            self.set_flight_planner(flight_planner)

    def update_content(self):
        for i, f in enumerate(self.flight_planner.flights):
            self.flightitems[i].update(f)

    def setup_content(self, row=0):
        for i, f in enumerate(self.flight_planner.flights):
            item = QFlightItem(f)
            self.model.appendRow(item)
            self.flightitems.append(item)
        self.setSelectedFlight(row)
        self.repaint()

    def setSelectedFlight(self, row):
        self.selectionModel().clearSelection()
        index = self.model.index(row, 0)
        if not index.isValid():
            index = self.model.index(0, 0)
        self.selectionModel().setCurrentIndex(index, QItemSelectionModel.Select)
        self.repaint()

    def clear_layout(self):
        self.model.removeRows(0, self.model.rowCount())

    def set_flight_planner(self, flight_planner: FlightPlanner, row=0):
        self.clear_layout()
        self.flight_planner = flight_planner
        if self.flight_planner:
            self.setup_content(row)
