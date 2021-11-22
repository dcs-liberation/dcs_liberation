from datetime import timedelta

from PySide2.QtCore import QItemSelectionModel, QPoint
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QHeaderView, QTableView

from game.ato.package import Package
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flight import Flight
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import QWaypointItem


class QFlightWaypointList(QTableView):
    def __init__(self, package: Package, flight: Flight):
        super().__init__()
        self.package = package
        self.flight = flight

        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Name", "Alt", "TOT/DEPART"])

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.update_list()

        self.selectionModel().setCurrentIndex(
            self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select
        )

    def update_list(self):
        # We need to keep just the row and rebuild the index later because the
        # QModelIndex will not be valid after the model is cleared.
        current_index = self.currentIndex().row()
        self.model.clear()

        self.model.setHorizontalHeaderLabels(["Name", "Alt", "TOT/DEPART"])

        waypoints = self.flight.flight_plan.waypoints
        for row, waypoint in enumerate(waypoints):
            self.add_waypoint_row(row, self.flight, waypoint)
        self.selectionModel().setCurrentIndex(
            self.model.index(current_index, 0), QItemSelectionModel.Select
        )
        self.resizeColumnsToContents()
        total_column_width = self.verticalHeader().width() + self.lineWidth()
        for i in range(0, self.model.columnCount()):
            total_column_width += self.columnWidth(i) + self.lineWidth()
        self.setFixedWidth(total_column_width)

    def add_waypoint_row(
        self, row: int, flight: Flight, waypoint: FlightWaypoint
    ) -> None:
        self.model.insertRow(self.model.rowCount())

        self.model.setItem(row, 0, QWaypointItem(waypoint, row))

        altitude = int(waypoint.alt.feet)
        altitude_type = "AGL" if waypoint.alt_type == "RADIO" else "MSL"
        altitude_item = QStandardItem(f"{altitude} ft {altitude_type}")
        altitude_item.setEditable(False)
        self.model.setItem(row, 1, altitude_item)

        tot = self.tot_text(flight, waypoint)
        tot_item = QStandardItem(tot)
        tot_item.setEditable(False)
        self.model.setItem(row, 2, tot_item)

    def tot_text(self, flight: Flight, waypoint: FlightWaypoint) -> str:
        if waypoint.waypoint_type == FlightWaypointType.TAKEOFF:
            return self.takeoff_text(flight)
        prefix = ""
        time = flight.flight_plan.tot_for_waypoint(waypoint)
        if time is None:
            prefix = "Depart "
            time = flight.flight_plan.depart_time_for_waypoint(waypoint)
        if time is None:
            return ""
        time = timedelta(seconds=int(time.total_seconds()))
        return f"{prefix}T+{time}"

    @staticmethod
    def takeoff_text(flight: Flight) -> str:
        takeoff_time = flight.flight_plan.takeoff_time()
        # Handle custom flight plans where we can't estimate the takeoff time.
        if takeoff_time is None:
            takeoff_time = timedelta()
        start_time = timedelta(seconds=int(takeoff_time.total_seconds()))
        return f"T+{start_time}"
