from PySide2.QtWidgets import QLabel, QGroupBox, QLineEdit, QGridLayout

from game import db
from gen.flights.flight import Flight
from qt_ui.uiconstants import AIRCRAFT_ICONS


class QFlightTypeTaskInfo(QGroupBox):

    def __init__(self, flight: Flight):
        super(QFlightTypeTaskInfo, self).__init__("Flight")
        self.flight = flight

        layout = QGridLayout()

        self.aircraft_icon = QLabel()
        if db.unit_type_name(self.flight.unit_type) in AIRCRAFT_ICONS:
            self.aircraft_icon.setPixmap(AIRCRAFT_ICONS[db.unit_type_name(self.flight.unit_type)])

        self.task = QLabel("Task :")
        self.task_type = QLabel(flight.flight_type.name)
        self.task_type.setProperty("style", flight.flight_type.name)

        self.name = QLineEdit()
        self.name.setText(flight.name)
        self.name.textChanged.connect(self.name_changed)
        # self.sette

        layout.addWidget(self.aircraft_icon, 0, 0)

        layout.addWidget(QLabel("Name :"), 1, 0)
        layout.addWidget(self.name, 1, 1)

        layout.addWidget(self.task, 2, 0)
        layout.addWidget(self.task_type, 2, 1)

        self.setLayout(layout)

    def name_changed(self, new_name):
        self.flight.name = new_name
