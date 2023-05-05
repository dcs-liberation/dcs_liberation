from __future__ import annotations

from PySide6.QtWidgets import QComboBox

from game.ato import FlightType
from game.dcs.aircrafttype import AircraftType
from game.squadrons import Squadron


class PrimaryTaskSelector(QComboBox):
    def __init__(self, aircraft: AircraftType | None) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.set_aircraft(aircraft)

    @staticmethod
    def for_squadron(squadron: Squadron) -> PrimaryTaskSelector:
        selector = PrimaryTaskSelector(squadron.aircraft)
        selector.setCurrentText(squadron.primary_task.value)
        return selector

    def set_aircraft(self, aircraft: AircraftType | None) -> None:
        self.clear()
        if aircraft is None:
            self.addItem("Select aircraft type first", None)
            self.setEnabled(False)
            self.update()
            return

        self.setEnabled(True)
        for task in aircraft.iter_task_capabilities():
            self.addItem(task.value, task)
        self.model().sort(0)
        self.setEnabled(True)
        self.update()

    @property
    def selected_task(self) -> FlightType | None:
        return self.currentData()
