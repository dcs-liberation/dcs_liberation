"""Combo box for selecting a flight's task type."""
from PySide2.QtWidgets import QComboBox

from gen.flights.flight import FlightType


class QFlightTypeComboBox(QComboBox):
    """Combo box for selecting a flight task type."""

    def __init__(self) -> None:
        super().__init__()
        self.addItem("CAP [Combat Air Patrol]", userData=FlightType.CAP)
        self.addItem("BARCAP [Barrier Combat Air Patrol]", userData=FlightType.BARCAP)
        self.addItem("TARCAP [Target Combat Air Patrol]", userData=FlightType.TARCAP)
        self.addItem("INTERCEPT [Interception]", userData=FlightType.INTERCEPTION)
        self.addItem("CAS [Close Air Support]", userData=FlightType.CAS)
        self.addItem("BAI [Battlefield Interdiction]", userData=FlightType.BAI)
        self.addItem("SEAD [Suppression of Enemy Air Defenses]", userData=FlightType.SEAD)
        self.addItem("DEAD [Destruction of Enemy Air Defenses]", userData=FlightType.DEAD)
        self.addItem("STRIKE [Strike]", userData=FlightType.STRIKE)
        self.addItem("ANTISHIP [Antiship Attack]", userData=FlightType.ANTISHIP)
        self.model().sort(0)
