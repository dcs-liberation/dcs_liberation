from typing import List

from PySide2.QtGui import QStandardItem


class QWaypointItem(QStandardItem):

    def __init__(self, point: List[int]):
        super(QWaypointItem, self).__init__()

        self.setText("X: " + str(int(point[0])) + "; Y: " + str(int(point[1])) + "; Alt: " + str(int(point[2])) + "m")

