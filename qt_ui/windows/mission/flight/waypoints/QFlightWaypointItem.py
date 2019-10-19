from typing import List

from PySide2.QtGui import QStandardItem

from gen.flights.flight import FlightWaypoint


class QWaypointItem(QStandardItem):

    def __init__(self, point: FlightWaypoint):
        super(QWaypointItem, self).__init__()
        self.setText('{0: <16}'.format(point.description) + " -- [X: " + str(int(point.x)) + "; Y: " + str(int(point.y)) + "; Alt: " + str(int(point.alt)) + "m]")

