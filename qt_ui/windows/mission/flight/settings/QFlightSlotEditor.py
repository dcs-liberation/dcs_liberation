from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QSpinBox, QGridLayout


class QFlightSlotEditor(QGroupBox):

    def __init__(self, flight, game):
        super(QFlightSlotEditor, self).__init__("Slots")
        self.flight = flight
        self.game = game

        layout = QGridLayout()

        self.aircraft_count = QLabel("Aircraft count :")
        self.aircraft_count_spinner = QSpinBox()
        self.aircraft_count_spinner.setMinimum(1)
        self.aircraft_count_spinner.setMaximum(4)
        self.aircraft_count_spinner.setValue(flight.count)
        self.aircraft_count_spinner.valueChanged.connect(self._changed_aircraft_count)

        self.client_count = QLabel("Client slots count :")
        self.client_count_spinner = QSpinBox()
        self.client_count_spinner.setMinimum(0)
        self.client_count_spinner.setMaximum(4)
        self.client_count_spinner.setValue(flight.client_count)
        self.client_count_spinner.valueChanged.connect(self._changed_client_count)

        if not self.flight.unit_type.flyable:
            self.client_count_spinner.setValue(0)
            self.client_count_spinner.setEnabled(False)

        layout.addWidget(self.aircraft_count, 0, 0)
        layout.addWidget(self.aircraft_count_spinner, 0, 1)

        layout.addWidget(self.client_count, 1, 0)
        layout.addWidget(self.client_count_spinner, 1, 1)

        self.setLayout(layout)

    def _changed_aircraft_count(self):
        self.flight.count = int(self.aircraft_count_spinner.value())
        # TODO check if enough aircraft are available

    def _changed_client_count(self):
        self.flight.client_count = int(self.client_count_spinner.value())
        self._cap_client_count()

    def _cap_client_count(self):
        if self.flight.client_count > self.flight.count:
            self.flight.client_count = self.flight.count
            self.client_count_spinner.setValue(self.flight.client_count)