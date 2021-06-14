from __future__ import annotations

from dataclasses import dataclass
from typing import Type, Union

import dcs
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QTextBrowser,
    QFrame,
)
from dcs.unittype import VehicleType

import gen.flights.ai_flight_planner_db
from game import db
from game.dcs.aircrafttype import AircraftType
from game.game import Game
from gen.flights.flight import FlightType
from qt_ui.uiconstants import AIRCRAFT_BANNERS, VEHICLE_BANNERS


@dataclass(frozen=True)
class UnitInfo:
    name: str
    description: str
    introduction_year: str
    origin: str
    manufacturer: str
    role: str

    @classmethod
    def from_unit_type(
        cls, country: str, unit_type: Union[AircraftType, Type[VehicleType]]
    ) -> UnitInfo:
        if isinstance(unit_type, AircraftType):
            return cls.from_aircraft(unit_type)
        else:
            return cls.from_vehicle_type(country, unit_type)

    @classmethod
    def from_aircraft(cls, aircraft: AircraftType) -> UnitInfo:
        return UnitInfo(
            aircraft.name,
            aircraft.description,
            aircraft.year_introduced,
            aircraft.country_of_origin,
            aircraft.manufacturer,
            aircraft.role,
        )

    @classmethod
    def from_vehicle_type(cls, country: str, unit_type: Type[VehicleType]) -> UnitInfo:
        name = db.unit_get_expanded_info(country, unit_type, "name")
        manufacturer = db.unit_get_expanded_info(country, unit_type, "manufacturer")
        origin = db.unit_get_expanded_info(country, unit_type, "country-of-origin")
        role = db.unit_get_expanded_info(country, unit_type, "role")
        introduction = db.unit_get_expanded_info(
            country, unit_type, "year-of-variant-introduction"
        )
        description = db.unit_get_expanded_info(country, unit_type, "text")
        return UnitInfo(
            name,
            description,
            introduction,
            origin,
            manufacturer,
            role,
        )


class QUnitInfoWindow(QDialog):
    def __init__(
        self, game: Game, unit_type: Union[AircraftType, Type[VehicleType]]
    ) -> None:
        super().__init__()
        self.setModal(True)
        self.game = game
        self.unit_type = unit_type
        if isinstance(unit_type, AircraftType):
            self.name = unit_type.name
        else:
            self.name = db.unit_get_expanded_info(
                self.game.player_country, self.unit_type, "name"
            )
        self.setWindowTitle(f"Unit Info: {self.name}")
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.setMinimumHeight(570)
        self.setMaximumWidth(640)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.layout = QGridLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 720, 360)

        pixmap = None

        if isinstance(self.unit_type, AircraftType):
            pixmap = AIRCRAFT_BANNERS.get(self.unit_type.dcs_id)
        elif dcs.vehicles.vehicle_map.get(self.unit_type.id) is not None:
            pixmap = VEHICLE_BANNERS.get(self.unit_type.id)
        if pixmap is None:
            pixmap = AIRCRAFT_BANNERS.get("Missing")
        header.setPixmap(pixmap.scaled(header.width(), header.height()))
        self.layout.addWidget(header, 0, 0)

        self.gridLayout = QGridLayout()

        # Build the topmost details grid.
        self.details_grid = QFrame()
        self.details_grid_layout = QGridLayout()
        self.details_grid_layout.setMargin(0)

        unit_info = UnitInfo.from_unit_type(self.game.player_country, self.unit_type)
        self.name_box = QLabel(
            f"<b>Name:</b> {unit_info.manufacturer} {unit_info.name}"
        )
        self.name_box.setProperty("style", "info-element")

        self.country_box = QLabel(f"<b>Country of Origin:</b> {unit_info.origin}")
        self.country_box.setProperty("style", "info-element")

        self.role_box = QLabel(f"<b>Role:</b> {unit_info.role}")
        self.role_box.setProperty("style", "info-element")

        self.year_box = QLabel(
            f"<b>Variant Introduction:</b> {unit_info.introduction_year}"
        )
        self.year_box.setProperty("style", "info-element")

        self.details_grid_layout.addWidget(self.name_box, 0, 0)
        self.details_grid_layout.addWidget(self.country_box, 0, 1)
        self.details_grid_layout.addWidget(self.role_box, 1, 0)
        self.details_grid_layout.addWidget(self.year_box, 1, 1)

        self.details_grid.setLayout(self.details_grid_layout)

        self.gridLayout.addWidget(self.details_grid, 1, 0)

        # If it's an aircraft, include the task list.
        if isinstance(unit_type, AircraftType):
            self.tasks_box = QLabel(
                f"<b>In-Game Tasks:</b> {self.generateAircraftTasks()}"
            )
            self.tasks_box.setProperty("style", "info-element")
            self.gridLayout.addWidget(self.tasks_box, 2, 0)

        # Finally, add the description box.
        self.details_text = QTextBrowser()
        self.details_text.setProperty("style", "info-desc")
        self.details_text.setText(unit_info.description)
        self.gridLayout.addWidget(self.details_text, 3, 0)

        self.layout.addLayout(self.gridLayout, 1, 0)
        self.setLayout(self.layout)

    def generateAircraftTasks(self) -> str:
        aircraft_tasks = ""
        unit_type = self.unit_type.dcs_unit_type
        if unit_type in gen.flights.ai_flight_planner_db.CAP_CAPABLE:
            aircraft_tasks = (
                aircraft_tasks
                + f"{FlightType.BARCAP}, {FlightType.ESCORT}, {FlightType.INTERCEPTION}, {FlightType.SWEEP}, {FlightType.TARCAP}, "
            )
        if unit_type in gen.flights.ai_flight_planner_db.CAS_CAPABLE:
            aircraft_tasks = (
                aircraft_tasks
                + f"{FlightType.CAS}, {FlightType.BAI}, {FlightType.OCA_AIRCRAFT}, "
            )
        if unit_type in gen.flights.ai_flight_planner_db.SEAD_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.SEAD}, "
        if unit_type in gen.flights.ai_flight_planner_db.DEAD_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.DEAD}, "
        if unit_type in gen.flights.ai_flight_planner_db.ANTISHIP_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.ANTISHIP}, "
        if unit_type in gen.flights.ai_flight_planner_db.RUNWAY_ATTACK_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.OCA_RUNWAY}, "
        if unit_type in gen.flights.ai_flight_planner_db.STRIKE_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.STRIKE}, "
        if unit_type in gen.flights.ai_flight_planner_db.REFUELING_CAPABALE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.REFUELING}, "
        return aircraft_tasks[:-2]
