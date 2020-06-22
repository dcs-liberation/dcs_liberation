from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QSpinBox


class QFlightDepartureEditor(QGroupBox):

    def __init__(self, flight):
        super(QFlightDepartureEditor, self).__init__("Departure")
        self.flight = flight

        layout = QHBoxLayout()
        self.depart_from = QLabel("Departing from <b>" + self.flight.from_cp.name + "</b>")
        self.depart_at_t = QLabel("At T +")
        self.minutes = QLabel(" minutes")

        self.departure_delta = QSpinBox(self)
        self.departure_delta.setMinimum(0)
        self.departure_delta.setMaximum(120)
        self.departure_delta.setValue(self.flight.scheduled_in)
        self.departure_delta.valueChanged.connect(self.change_scheduled)

        layout.addWidget(self.depart_from)
        layout.addWidget(self.depart_at_t)
        layout.addWidget(self.departure_delta)
        layout.addWidget(self.minutes)
        self.setLayout(layout)

        self.changed = self.departure_delta.valueChanged

    def change_scheduled(self):
        self.flight.scheduled_in = int(self.departure_delta.value())
