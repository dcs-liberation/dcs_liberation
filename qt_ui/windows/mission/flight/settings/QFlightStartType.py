from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QComboBox, QLabel
from dcs.mission import StartType

from gen.flights.flight import Flight


class QFlightStartType(QGroupBox):

    def __init__(self, flight:Flight):
        super(QFlightStartType, self).__init__()

        self.flight = flight

        self.layout = QHBoxLayout()
        self.start_type_label = QLabel("Start type : ")
        self.start_type = QComboBox()

        for i, st in enumerate([b for b in ["Cold", "Warm", "Runway", "In Flight"]]):
            self.start_type.addItem(st, st)
            if flight.start_type == st:
                self.start_type.setCurrentIndex(i)

        self.start_type.currentTextChanged.connect(self._on_start_type_selected)
        self.layout.addWidget(self.start_type_label)
        self.layout.addWidget(self.start_type)
        self.setLayout(self.layout)

    def _on_start_type_selected(self):
        selected = self.start_type.currentData()
        self.flight.start_type = selected



