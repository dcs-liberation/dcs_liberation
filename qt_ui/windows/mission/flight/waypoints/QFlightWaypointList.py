from PySide2.QtCore import QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QListView

from gen.flights.flight import Flight, FlightWaypoint
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import QWaypointItem


class QFlightWaypointList(QListView):

    def __init__(self, flight: Flight):
        super(QFlightWaypointList, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.flight = flight

        if len(self.flight.points) > 0:
            self.selectedPoint = self.flight.points[0]
        self.update_list()

        self.selectionModel().setCurrentIndex(self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select)
        self.selectionModel().selectionChanged.connect(self.on_waypoint_selected_changed)

    def on_waypoint_selected_changed(self):
        index = self.selectionModel().currentIndex().row()

    def update_list(self):
        self.model.clear()
        takeoff = FlightWaypoint(self.flight.from_cp.position.x, self.flight.from_cp.position.y, 0)
        takeoff.description = "Take Off"
        self.model.appendRow(QWaypointItem(takeoff))
        for i, point in enumerate(self.flight.points):
            self.model.appendRow(QWaypointItem(point))
        self.selectionModel().setCurrentIndex(self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select)