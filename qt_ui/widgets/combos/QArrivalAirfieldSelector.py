"""Combo box for selecting a departure airfield."""
from typing import Iterable

from PySide2.QtWidgets import QComboBox
from dcs.planes import PlaneType

from game import db
from game.theater.controlpoint import ControlPoint


class QArrivalAirfieldSelector(QComboBox):
    """A combo box for selecting a flight's arrival or divert airfield.

    The combo box will automatically be populated with all airfields the given
    aircraft type is able to land at.
    """

    def __init__(self, destinations: Iterable[ControlPoint],
                 aircraft: PlaneType, optional_text: str) -> None:
        super().__init__()
        self.destinations = list(destinations)
        self.aircraft = aircraft
        self.optional_text = optional_text
        self.rebuild_selector()
        self.setCurrentIndex(0)

    def change_aircraft(self, aircraft: PlaneType) -> None:
        if self.aircraft == aircraft:
            return
        self.aircraft = aircraft
        self.rebuild_selector()

    def valid_destination(self, destination: ControlPoint) -> bool:
        if destination.is_carrier and self.aircraft not in db.CARRIER_CAPABLE:
            return False
        if destination.is_lha and self.aircraft not in db.LHA_CAPABLE:
            return False
        return True

    def rebuild_selector(self) -> None:
        self.clear()
        for destination in self.destinations:
            if self.valid_destination(destination):
                self.addItem(destination.name, destination)
        self.model().sort(0)
        self.insertItem(0, self.optional_text, None)
        self.update()
