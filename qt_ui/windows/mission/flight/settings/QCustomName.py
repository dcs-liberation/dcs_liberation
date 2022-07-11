from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QLabel

from game.ato.scheduledflight import ScheduledFlight


class QFlightCustomName(QGroupBox):
    def __init__(self, flight: ScheduledFlight):
        super(QFlightCustomName, self).__init__()

        self.flight = flight

        self.layout = QHBoxLayout()
        self.custom_name_label = QLabel(f"Custom Name: {flight.custom_name}")
        self.layout.addWidget(self.custom_name_label)
        self.setLayout(self.layout)
