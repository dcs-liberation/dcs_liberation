"""Combo box for selecting aircraft types."""
from typing import Iterable, Type

from PySide2.QtWidgets import QComboBox

from dcs.unittype import FlyingType

from game import Game, db

class QAircraftTypeSelector(QComboBox):
    """Combo box for selecting among the given aircraft types."""

    def __init__(self, aircraft_types: Iterable[Type[FlyingType]], country: str) -> None:
        super().__init__()
        for aircraft in aircraft_types:
            self.addItem(f"{db.unit_pretty_name(country, aircraft)}", userData=aircraft)
        self.model().sort(0)
