import logging
from typing import Type

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QMovie, QPixmap
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextBrowser,
    QFrame,
)
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dcs.unittype import UnitType, FlyingType, VehicleType
import dcs
from qt_ui.uiconstants import AIRCRAFT_BANNERS, VEHICLE_BANNERS

from game.game import Game
from game import db

import gen.flights.ai_flight_planner_db
from gen.flights.flight import FlightType


class QUnitInfoWindow(QDialog):
    def __init__(self, game: Game, unit_type: Type[UnitType]) -> None:
        super(QUnitInfoWindow, self).__init__()
        self.setModal(True)
        self.game = game
        self.unit_type = unit_type
        self.setWindowTitle(
            f"Unit Info: {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'name')}"
        )
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.setMinimumHeight(570)
        self.setMaximumWidth(640)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 720, 360)

        pixmap = None

        if (
            dcs.planes.plane_map.get(self.unit_type.id) is not None
            or dcs.helicopters.helicopter_map.get(self.unit_type.id) is not None
        ):
            pixmap = AIRCRAFT_BANNERS.get(self.unit_type.id)
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

        self.name_box = QLabel(
            f"<b>Name:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'manufacturer')} {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'name')}"
        )
        self.name_box.setProperty("style", "info-element")

        self.country_box = QLabel(
            f"<b>Country of Origin:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'country-of-origin')}"
        )
        self.country_box.setProperty("style", "info-element")

        self.role_box = QLabel(
            f"<b>Role:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'role')}"
        )
        self.role_box.setProperty("style", "info-element")

        self.year_box = QLabel(
            f"<b>Variant Introduction:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'year-of-variant-introduction')}"
        )
        self.year_box.setProperty("style", "info-element")

        self.details_grid_layout.addWidget(self.name_box, 0, 0)
        self.details_grid_layout.addWidget(self.country_box, 0, 1)
        self.details_grid_layout.addWidget(self.role_box, 1, 0)
        self.details_grid_layout.addWidget(self.year_box, 1, 1)

        self.details_grid.setLayout(self.details_grid_layout)

        self.gridLayout.addWidget(self.details_grid, 1, 0)

        # If it's an aircraft, include the task list.
        if (
            dcs.planes.plane_map.get(self.unit_type.id) is not None
            or dcs.helicopters.helicopter_map.get(self.unit_type.id) is not None
        ):
            self.tasks_box = QLabel(
                f"<b>In-Game Tasks:</b> {self.generateAircraftTasks()}"
            )
            self.tasks_box.setProperty("style", "info-element")
            self.gridLayout.addWidget(self.tasks_box, 2, 0)

        # Finally, add the description box.
        self.details_text = QTextBrowser()
        self.details_text.setProperty("style", "info-desc")
        self.details_text.setText(
            db.unit_get_expanded_info(self.game.player_country, self.unit_type, "text")
        )
        self.gridLayout.addWidget(self.details_text, 3, 0)

        self.layout.addLayout(self.gridLayout, 1, 0)
        self.setLayout(self.layout)

    def generateAircraftTasks(self) -> str:
        aircraft_tasks = ""
        if self.unit_type in gen.flights.ai_flight_planner_db.CAP_CAPABLE:
            aircraft_tasks = (
                aircraft_tasks
                + f"{FlightType.BARCAP}, {FlightType.ESCORT}, {FlightType.INTERCEPTION}, {FlightType.SWEEP}, {FlightType.TARCAP}, "
            )
        if self.unit_type in gen.flights.ai_flight_planner_db.CAS_CAPABLE:
            aircraft_tasks = (
                aircraft_tasks
                + f"{FlightType.CAS}, {FlightType.BAI}, {FlightType.OCA_AIRCRAFT}, "
            )
        if self.unit_type in gen.flights.ai_flight_planner_db.SEAD_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.SEAD}, "
        if self.unit_type in gen.flights.ai_flight_planner_db.DEAD_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.DEAD}, "
        if self.unit_type in gen.flights.ai_flight_planner_db.ANTISHIP_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.ANTISHIP}, "
        if self.unit_type in gen.flights.ai_flight_planner_db.RUNWAY_ATTACK_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.OCA_RUNWAY}, "
        if self.unit_type in gen.flights.ai_flight_planner_db.STRIKE_CAPABLE:
            aircraft_tasks = aircraft_tasks + f"{FlightType.STRIKE}, "
        return aircraft_tasks[:-2]
