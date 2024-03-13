from PySide6.QtWidgets import QComboBox
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato.flightmember import FlightMember
from .missingpropertydataerror import MissingPropertyDataError


class PropertyComboBox(QComboBox):
    def __init__(
        self, flight_member: FlightMember, prop: UnitPropertyDescription
    ) -> None:
        super().__init__()
        self.flight_member = flight_member
        self.prop = prop

        if prop.values is None:
            raise MissingPropertyDataError("values cannot be None")
        if prop.default is None:
            raise MissingPropertyDataError("default cannot be None")

        current_value = self.flight_member.properties.get(
            self.prop.identifier, self.prop.default
        )

        for ident, text in self.prop.values.items():
            self.addItem(text, ident)
            if ident == current_value:
                self.setCurrentText(text)

        self.currentIndexChanged.connect(self.on_selection_changed)

    def on_selection_changed(self, _index: int) -> None:
        self.flight_member.properties[self.prop.identifier] = self.currentData()

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        self.setCurrentText(
            self.flight_member.properties.get(
                self.prop.identifier, self.prop.values[self.prop.default]
            )
        )
