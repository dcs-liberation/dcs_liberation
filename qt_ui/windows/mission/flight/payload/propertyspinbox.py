from PySide6.QtWidgets import QSpinBox
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato import Flight
from .missingpropertydataerror import MissingPropertyDataError


class PropertySpinBox(QSpinBox):
    def __init__(self, flight: Flight, prop: UnitPropertyDescription) -> None:
        super().__init__()
        self.flight = flight
        self.prop = prop

        if prop.minimum is None:
            raise MissingPropertyDataError("minimum cannot be None")
        if prop.maximum is None:
            raise MissingPropertyDataError("maximum cannot be None")
        if prop.default is None:
            raise MissingPropertyDataError("default cannot be None")

        self.setMinimum(prop.minimum)
        self.setMaximum(prop.maximum)
        self.setValue(self.flight.props.get(self.prop.identifier, self.prop.default))

        self.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, value: int) -> None:
        self.flight.props[self.prop.identifier] = value
