from PySide2.QtCore import QSize
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QListView

from gen.flights.ai_flight_planner import FlightPlanner
from qt_ui.windows.mission.QFlightItem import QFlightItem


class QPlannedFlightsView(QListView):

    def __init__(self, flight_planner: FlightPlanner):
        super(QPlannedFlightsView, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.setIconSize(QSize(91, 24))
        if flight_planner:
            self.set_flight_planner(flight_planner)

    def update_content(self):
        for i, f in enumerate(self.flight_planner.flights):
            self.model.appendRow(QFlightItem(f))

    def clear_layout(self):
        self.model.removeRows(0, self.model.rowCount())

    def set_flight_planner(self, flight_planner: FlightPlanner):
        self.clear_layout()
        self.flight_planner = flight_planner
        if self.flight_planner:
            self.update_content()
