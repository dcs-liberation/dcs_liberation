"""Combo box for selecting squadrons."""
from typing import Optional

from PySide2.QtWidgets import QComboBox

from game.dcs.aircrafttype import AircraftType
from game.squadrons.airwing import AirWing
from game.ato.flighttype import FlightType


class SquadronSelector(QComboBox):
    """Combo box for selecting squadrons compatible with the given requirements."""

    def __init__(
        self,
        air_wing: AirWing,
        task: Optional[FlightType],
        aircraft: Optional[AircraftType],
    ) -> None:
        super().__init__()
        self.air_wing = air_wing

        self.model().sort(0)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.update_items(task, aircraft)

    @property
    def aircraft_available(self) -> int:
        squadron = self.currentData()
        if squadron is None:
            return 0
        return squadron.untasked_aircraft

    def update_items(
        self, task: Optional[FlightType], aircraft: Optional[AircraftType]
    ) -> None:
        current_squadron = self.currentData()
        self.blockSignals(True)
        try:
            self.clear()
        finally:
            self.blockSignals(False)
        if task is None:
            self.addItem("No task selected", None)
            return
        if aircraft is None:
            self.addItem("No aircraft selected", None)
            return

        for squadron in self.air_wing.squadrons_for(aircraft):
            if task in squadron.mission_types and squadron.untasked_aircraft:
                self.addItem(f"{squadron.location}: {squadron}", squadron)

        if self.count() == 0:
            self.addItem("No capable aircraft available", None)
            return

        if current_squadron is not None:
            self.setCurrentText(f"{current_squadron.location}: {current_squadron}")
