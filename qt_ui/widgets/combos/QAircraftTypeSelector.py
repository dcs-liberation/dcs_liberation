"""Combo box for selecting aircraft types."""
from typing import Iterable, Type

from PySide2.QtWidgets import QComboBox
from dcs.unittype import FlyingType

from game import db
from gen.flights.ai_flight_planner_db import aircraft_for_task
from gen.flights.flight import FlightType


class QAircraftTypeSelector(QComboBox):
    """Combo box for selecting among the given aircraft types."""

    def __init__(
        self,
        aircraft_types: Iterable[Type[FlyingType]],
        country: str,
        mission_type: FlightType,
    ) -> None:
        super().__init__()

        self.model().sort(0)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.country = country
        self.update_items(mission_type, aircraft_types)

    def update_items(self, mission_type: FlightType, aircraft_types):
        current_aircraft = self.currentData()
        self.clear()
        for aircraft in aircraft_types:
            if aircraft in aircraft_for_task(mission_type):
                self.addItem(f"{aircraft}", userData=aircraft)
        current_aircraft_index = self.findData(current_aircraft)
        if current_aircraft_index != -1:
            self.setCurrentIndex(current_aircraft_index)
        if self.count() == 0:
            self.addItem("No capable aircraft available", userData=None)
