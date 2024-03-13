from PySide6.QtWidgets import QCheckBox
from dcs.unitpropertydescription import UnitPropertyDescription

from game.ato.flightmember import FlightMember
from .missingpropertydataerror import MissingPropertyDataError


class PropertyCheckBox(QCheckBox):
    def __init__(
        self, flight_member: FlightMember, prop: UnitPropertyDescription
    ) -> None:
        super().__init__()
        self.flight_member = flight_member
        self.prop = prop

        if prop.default is None:
            raise MissingPropertyDataError("default cannot be None")

        self.setChecked(
            self.flight_member.properties.get(self.prop.identifier, self.prop.default)
        )
        self.toggled.connect(self.on_toggle)

    def on_toggle(self, checked: bool) -> None:
        self.flight_member.properties[self.prop.identifier] = checked

    def set_flight_member(self, flight_member: FlightMember) -> None:
        self.flight_member = flight_member
        self.setChecked(
            self.flight_member.properties.get(self.prop.identifier, self.prop.default)
        )
