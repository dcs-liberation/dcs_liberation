"""Combo box for selecting aircraft types."""
from typing import Iterable, Type

from PySide2.QtWidgets import QComboBox

from dcs.unittype import FlyingType

from gen.flights.flight import FlightType

import gen.flights.ai_flight_planner_db

from game import Game, db

class QAircraftTypeSelector(QComboBox):
    """Combo box for selecting among the given aircraft types."""

    def __init__(self, aircraft_types: Iterable[Type[FlyingType]], country: str, mission_type: str) -> None:
        super().__init__()

        self.model().sort(0)
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.country = country
        self.updateItems(mission_type, aircraft_types)

    def updateItems(self, mission_type: str, aircraft_types):
        current_aircraft = self.currentData()
        self.clear()
        for aircraft in aircraft_types:
            if mission_type in [FlightType.BARCAP, FlightType.ESCORT, FlightType.INTERCEPTION, FlightType.SWEEP, FlightType.TARCAP]:
                if aircraft in gen.flights.ai_flight_planner_db.CAP_CAPABLE:
                    self.addItem(f"{db.unit_pretty_name(self.country, aircraft)}", userData=aircraft)
            elif mission_type in [FlightType.CAS, FlightType.BAI, FlightType.OCA_AIRCRAFT]:
                if aircraft in gen.flights.ai_flight_planner_db.CAS_CAPABLE:
                    self.addItem(f"{db.unit_pretty_name(self.country, aircraft)}", userData=aircraft)
            elif mission_type in [FlightType.SEAD, FlightType.DEAD]:
                if aircraft in gen.flights.ai_flight_planner_db.SEAD_CAPABLE:
                    self.addItem(f"{db.unit_pretty_name(self.country, aircraft)}", userData=aircraft)
            elif mission_type in [FlightType.STRIKE]:
                if aircraft in [gen.flights.ai_flight_planner_db.STRIKE_CAPABLE, gen.flights.ai_flight_planner_db.TRANSPORT_CAPABLE]:
                    self.addItem(f"{db.unit_pretty_name(self.country, aircraft)}", userData=aircraft)
            elif mission_type in [FlightType.ANTISHIP]:
                if aircraft in gen.flights.ai_flight_planner_db.ANTISHIP_CAPABLE:
                    self.addItem(f"{db.unit_pretty_name(self.country, aircraft)}", userData=aircraft)
            elif mission_type in [FlightType.OCA_RUNWAY]:
                if aircraft in gen.flights.ai_flight_planner_db.RUNWAY_ATTACK_CAPABLE:
                    self.addItem(f"{db.unit_pretty_name(self.country, aircraft)}", userData=aircraft)
        current_aircraft_index = self.findData(current_aircraft)
        if current_aircraft_index != -1:
            self.setCurrentIndex(current_aircraft_index)
        if self.count() == 0:
            self.addItem("No capable aircraft available", userData=None)