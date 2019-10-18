from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QSpinBox, QGridLayout

from game import db
from qt_ui.uiconstants import AIRCRAFT_ICONS


class QFlightTypeTaskInfo(QGroupBox):

    def __init__(self, flight):
        super(QFlightTypeTaskInfo, self).__init__("Flight")
        self.flight = flight

        layout = QGridLayout()

        self.aircraft_icon = QLabel()
        if db.unit_type_name(self.flight.unit_type) in AIRCRAFT_ICONS:
            self.aircraft_icon.setPixmap(AIRCRAFT_ICONS[db.unit_type_name(self.flight.unit_type)])

        self.task = QLabel("Task :")
        self.task_type = QLabel(flight.flight_type.name)
        self.task_type.setProperty("style", flight.flight_type.name)

        layout.addWidget(self.aircraft_icon, 0, 0)

        layout.addWidget(self.task, 1, 0)
        layout.addWidget(self.task_type, 1, 1)

        self.setLayout(layout)
