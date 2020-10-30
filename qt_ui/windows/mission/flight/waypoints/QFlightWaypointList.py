import itertools

from PySide2.QtCore import QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QHeaderView, QTableView

from game.utils import meter_to_feet
from gen.ato import Package
from gen.flights.flight import Flight, FlightWaypoint
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import \
    QWaypointItem


class QFlightWaypointList(QTableView):

    def __init__(self, package: Package, flight: Flight):
        super().__init__()
        self.package = package
        self.flight = flight

        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model.setHorizontalHeaderLabels(["Name", "Alt", "TOT/DEPART"])

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        if len(self.flight.points) > 0:
            self.selectedPoint = self.flight.points[0]
        self.update_list()

        self.selectionModel().setCurrentIndex(self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select)
        self.selectionModel().selectionChanged.connect(self.on_waypoint_selected_changed)

    def on_waypoint_selected_changed(self):
        index = self.selectionModel().currentIndex().row()

    def update_list(self):
        self.model.clear()

        self.model.setHorizontalHeaderLabels(["Name", "Alt", "TOT/DEPART"])

        # The first waypoint is set up by pydcs at mission generation time, so
        # we need to add that waypoint manually.
        takeoff = FlightWaypoint(self.flight.from_cp.position.x,
                                 self.flight.from_cp.position.y, 0)
        takeoff.description = "Take Off"
        takeoff.name = takeoff.pretty_name = "Take Off from " + self.flight.from_cp.name
        takeoff.alt_type = "RADIO"

        waypoints = itertools.chain([takeoff], self.flight.points)
        for row, waypoint in enumerate(waypoints):
            self.add_waypoint_row(row, self.flight, waypoint)
        self.selectionModel().setCurrentIndex(self.indexAt(QPoint(1, 1)),
                                              QItemSelectionModel.Select)

    def add_waypoint_row(self, row: int, flight: Flight,
                         waypoint: FlightWaypoint) -> None:
        self.model.insertRow(self.model.rowCount())

        self.model.setItem(row, 0, QWaypointItem(waypoint, row))

        altitude = meter_to_feet(waypoint.alt)
        altitude_type = "AGL" if waypoint.alt_type == "RADIO" else "MSL"
        altitude_item = QStandardItem(f"{altitude} ft {altitude_type}")
        altitude_item.setEditable(False)
        self.model.setItem(row, 1, altitude_item)

        tot = self.tot_text(flight, waypoint)
        tot_item = QStandardItem(tot)
        tot_item.setEditable(False)
        self.model.setItem(row, 2, tot_item)

    @staticmethod
    def tot_text(flight: Flight, waypoint: FlightWaypoint) -> str:
        prefix = ""
        time = flight.flight_plan.tot_for_waypoint(waypoint)
        if time is None:
            prefix = "Depart "
            time = flight.flight_plan.depart_time_for_waypoint(waypoint)
        if time is None:
            return ""
        return f"{prefix}T+{time}"
