"""Combo box for selecting squadrons."""
from typing import Type, Optional

from PySide2.QtWidgets import QComboBox
from dcs.unittype import FlyingType

from game.squadrons import AirWing
from gen.flights.flight import FlightType


class SquadronSelector(QComboBox):
    """Combo box for selecting squadrons compatible with the given requirements."""

    def __init__(
        self,
        air_wing: AirWing,
        task: Optional[FlightType],
        aircraft: Optional[Type[FlyingType]],
    ) -> None:
        super().__init__()
        self.air_wing = air_wing

        self.model().sort(0)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.update_items(task, aircraft)

    def update_items(
        self, task: Optional[FlightType], aircraft: Optional[Type[FlyingType]]
    ) -> None:
        current_squadron = self.currentData()
        self.clear()
        if task is None:
            self.addItem("No task selected", None)
            return
        if aircraft is None:
            self.addItem("No aircraft selected", None)
            return

        for squadron in self.air_wing.squadrons_for(aircraft):
            if task in squadron.mission_types:
                self.addItem(f"{squadron}", squadron)

        if self.count() == 0:
            self.addItem("No capable aircraft available", None)
            return

        if current_squadron is not None:
            self.setCurrentText(f"{current_squadron}")
