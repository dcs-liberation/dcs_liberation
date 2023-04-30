from PySide6.QtCore import QItemSelectionModel, QPoint
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QHeaderView, QTableView

from game.ato.flight import Flight
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.flightwaypointtype import FlightWaypointType
from game.ato.package import Package
from game.utils import Distance
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import QWaypointItem


HEADER_LABELS = ["Name", "Alt (ft)", "Alt Type", "TOT/DEPART"]


class QFlightWaypointList(QTableView):
    def __init__(self, package: Package, flight: Flight):
        super().__init__()
        self.package = package
        self.flight = flight

        self.model = QStandardItemModel(self)
        self.model.itemChanged.connect(self.on_changed)
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(HEADER_LABELS)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.update_list()

        self.selectionModel().setCurrentIndex(
            self.indexAt(QPoint(1, 1)), QItemSelectionModel.Select
        )

    def update_list(self) -> None:
        # disconnect itemChanged signal from handler slot for making altitude changes
        # in advance updating waypoint list
        self.model.itemChanged.disconnect(self.on_changed)

        # We need to keep just the row and rebuild the index later because the
        # QModelIndex will not be valid after the model is cleared.
        current_index = self.currentIndex().row()
        self.model.clear()

        self.model.setHorizontalHeaderLabels(HEADER_LABELS)

        waypoints = self.flight.flight_plan.waypoints
        for row, waypoint in enumerate(waypoints):
            self._add_waypoint_row(row, self.flight, waypoint)
        self.selectionModel().setCurrentIndex(
            self.model.index(current_index, 0), QItemSelectionModel.Select
        )
        self.resizeColumnsToContents()
        total_column_width = self.verticalHeader().width() + self.lineWidth()
        for i in range(0, self.model.columnCount()):
            total_column_width += self.columnWidth(i) + self.lineWidth()
        self.setFixedWidth(total_column_width)

        # reconnect itemChanged signal to handler slot for making altitude changes
        self.model.itemChanged.connect(self.on_changed)

    def _add_waypoint_row(
        self, row: int, flight: Flight, waypoint: FlightWaypoint
    ) -> None:
        self.model.insertRow(self.model.rowCount())

        self.model.setItem(row, 0, QWaypointItem(waypoint, row))

        altitude = int(waypoint.alt.feet)
        altitude_item = QStandardItem(f"{altitude}")
        altitude_item.setEditable(True)
        self.model.setItem(row, 1, altitude_item)

        altitude_type = "AGL" if waypoint.alt_type == "RADIO" else "MSL"
        altitude_type_item = QStandardItem(f"{altitude_type}")
        altitude_type_item.setEditable(False)
        self.model.setItem(row, 2, altitude_type_item)

        tot = self.tot_text(flight, waypoint)
        tot_item = QStandardItem(tot)
        tot_item.setEditable(False)
        self.model.setItem(row, 3, tot_item)

    def on_changed(self) -> None:
        for i in range(self.model.rowCount()):
            altitude = self.model.item(i, 1).text()
            try:
                altitude_feet = float(altitude)
            except:
                continue
            self.flight.flight_plan.waypoints[i].alt = Distance.from_feet(altitude_feet)

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
        return f"{prefix}{time:%H:%M:%S}"

    @staticmethod
    def takeoff_text(flight: Flight) -> str:
        return f"{flight.flight_plan.takeoff_time():%H:%M:%S}"
