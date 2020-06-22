from PySide2.QtCore import QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QTableView, QHeaderView

from game.utils import meter_to_feet
from gen.flights.flight import Flight, FlightWaypoint
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import QWaypointItem


class QFlightWaypointList(QTableView):

    def __init__(self, flight: Flight):
        super(QFlightWaypointList, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model.setHorizontalHeaderLabels(["Name", "Alt"])

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

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
        self.model.setHorizontalHeaderLabels(["Name", "Alt"])
        takeoff = FlightWaypoint(self.flight.from_cp.position.x, self.flight.from_cp.position.y, 0)
        takeoff.description = "Take Off"
        takeoff.name = takeoff.pretty_name = "Take Off from " + self.flight.from_cp.name
        self.model.appendRow(QWaypointItem(takeoff, 0))
        self.model.setItem(0, 1, QStandardItem("0 ft AGL"))
        for i, point in enumerate(self.flight.points):
            self.model.insertRow(self.model.rowCount())
            self.model.setItem(self.model.rowCount()-1, 0, QWaypointItem(point, i + 1))
            self.model.setItem(self.model.rowCount()-1, 1, QStandardItem(str(meter_to_feet(point.alt)) + " ft " + str(["AGL" if point.alt_type == "RADIO" else "MSL"][0])))
        self.selectionModel().setCurrentIndex(self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select)