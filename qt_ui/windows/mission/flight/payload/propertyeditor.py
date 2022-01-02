from PySide2.QtWidgets import QGridLayout, QLabel

from game.ato import Flight
from .propertyselector import PropertySelector


class PropertyEditor(QGridLayout):
    def __init__(self, flight: Flight) -> None:
        super().__init__()
        self.flight = flight

        for row, prop in enumerate(flight.unit_type.iter_props()):
            self.addWidget(QLabel(prop.id), row, 0)
            self.addWidget(PropertySelector(self.flight, prop), row, 1)
