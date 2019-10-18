from PySide2.QtWidgets import QFrame, QGridLayout, QLabel

from gen.flights.flight import Flight


class QFlightWaypointTab(QFrame):

    def __init__(self, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.flight = flight
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Coming in two weeks"))
        self.setLayout(layout)
