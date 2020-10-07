"""Combo box for selecting aircraft types."""
from typing import Iterable

from PySide2.QtWidgets import QComboBox

from dcs.planes import PlaneType


class QAircraftTypeSelector(QComboBox):
    """Combo box for selecting among the given aircraft types."""

    def __init__(self, aircraft_types: Iterable[PlaneType]) -> None:
        super().__init__()
        for aircraft in aircraft_types:
            self.addItem(f"{aircraft.id}", userData=aircraft)
        self.model().sort(0)
