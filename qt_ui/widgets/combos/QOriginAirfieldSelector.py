"""Combo box for selecting a departure airfield."""
from typing import Iterable

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QComboBox
from dcs.unittype import FlyingType

from game.inventory import GlobalAircraftInventory
from game.theater.controlpoint import ControlPoint


class QOriginAirfieldSelector(QComboBox):
    """A combo box for selecting a flight's departure airfield.

    The combo box will automatically be populated with all departure airfields
    that have unassigned inventory of the given aircraft type.
    """

    availability_changed = Signal(int)

    def __init__(self, global_inventory: GlobalAircraftInventory,
                 origins: Iterable[ControlPoint],
                 aircraft: FlyingType) -> None:
        super().__init__()
        self.global_inventory = global_inventory
        self.origins = list(origins)
        self.aircraft = aircraft
        self.rebuild_selector()
        self.currentIndexChanged.connect(self.index_changed)

    def change_aircraft(self, aircraft: FlyingType) -> None:
        if self.aircraft == aircraft:
            return
        self.aircraft = aircraft
        self.rebuild_selector()

    def rebuild_selector(self) -> None:
        self.clear()
        for origin in self.origins:
            inventory = self.global_inventory.for_control_point(origin)
            available = inventory.available(self.aircraft)
            if available:
                self.addItem(f"{origin.name} ({available} available)", origin)
        self.model().sort(0)
        self.update()

    @property
    def available(self) -> int:
        origin = self.currentData()
        if origin is None:
            return 0
        inventory = self.global_inventory.for_control_point(origin)
        return inventory.available(self.aircraft)

    def index_changed(self, index: int) -> None:
        origin = self.itemData(index)
        if origin is None:
            return
        inventory = self.global_inventory.for_control_point(origin)
        self.availability_changed.emit(inventory.available(self.aircraft))
