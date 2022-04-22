"""Combo box for selecting aircraft types."""
from PySide2.QtWidgets import QComboBox
from game.dcs.aircrafttype import AircraftType


class QAircraftTypeSelector(QComboBox):
    """Combo box for selecting among the given aircraft types."""

    def __init__(self, aircraft_types: list[AircraftType]) -> None:
        super().__init__()

        self.model().sort(0)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.update_items(aircraft_types)

    def update_items(self, aircraft_types: list[AircraftType]):
        current_aircraft = self.currentData()
        self.clear()
        for aircraft in aircraft_types:
            self.addItem(f"{aircraft}", userData=aircraft)
        current_aircraft_index = self.findData(current_aircraft)
        if current_aircraft_index != -1:
            self.setCurrentIndex(current_aircraft_index)
        if self.count() == 0:
            self.addItem("No capable aircraft available", userData=None)
