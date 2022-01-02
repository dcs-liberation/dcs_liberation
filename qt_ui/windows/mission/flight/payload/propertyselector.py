from PySide2.QtWidgets import QComboBox

from game.ato import Flight
from game.dcs.unitproperty import UnitProperty


class PropertySelector(QComboBox):
    def __init__(self, flight: Flight, prop: UnitProperty) -> None:
        super().__init__()
        self.flight = flight
        self.prop = prop

        current_value = self.flight.props.get(self.prop.id, self.prop.default)

        for value in self.prop.values:
            self.addItem(value.id, value.value)
            if value.value == current_value:
                self.setCurrentText(value.id)

        self.currentIndexChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, _index: int) -> None:
        self.flight.props[self.prop.id] = self.currentData()
