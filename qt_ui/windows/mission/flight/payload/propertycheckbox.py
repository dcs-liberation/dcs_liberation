from PySide6.QtWidgets import QCheckBox
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato import Flight
from .missingpropertydataerror import MissingPropertyDataError


class PropertyCheckBox(QCheckBox):
    def __init__(self, flight: Flight, prop: UnitPropertyDescription) -> None:
        super().__init__()
        self.flight = flight
        self.prop = prop

        if prop.default is None:
            raise MissingPropertyDataError("default cannot be None")

        self.setChecked(self.flight.props.get(self.prop.identifier, self.prop.default))
        self.toggled.connect(self.on_toggle)

    def on_toggle(self, checked: bool) -> None:
        self.flight.props[self.prop.identifier] = checked
