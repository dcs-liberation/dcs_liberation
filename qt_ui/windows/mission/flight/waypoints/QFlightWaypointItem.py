from typing import List

from PySide2.QtGui import QStandardItem

from game.ato.flightwaypoint import FlightWaypoint


class QWaypointItem(QStandardItem):
    def __init__(self, point: FlightWaypoint, number):
        super(QWaypointItem, self).__init__()
        self.number = number
        self.setText("{:<16}".format(point.pretty_name))
        self.setEditable(False)
