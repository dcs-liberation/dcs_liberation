from PySide2.QtGui import QStandardItemModel
from PySide2.QtWidgets import QListView

from gen.flights.flight import Flight
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointItem import QWaypointItem


class QFlightWaypointList(QListView):

    def __init__(self, flight: Flight):
        super(QFlightWaypointList, self).__init__()
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.flight = flight

        self.model.appendRow(QWaypointItem([flight.from_cp.position.x, flight.from_cp.position.y, 0]))
        for i, point in enumerate(self.flight.points):
            self.model.appendRow(QWaypointItem(point))