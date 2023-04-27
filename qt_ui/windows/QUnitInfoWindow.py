from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QFrame, QGridLayout, QLabel, QTextBrowser

from game.dcs.aircrafttype import AircraftType
from game.dcs.groundunittype import GroundUnitType
from game.dcs.unittype import UnitType
from game.game import Game
from qt_ui.uiconstants import AIRCRAFT_BANNERS, VEHICLE_BANNERS


class QUnitInfoWindow(QDialog):
    def __init__(self, game: Game, unit_type: UnitType) -> None:
        super().__init__()
        self.setModal(True)
        self.game = game
        self.unit_type = unit_type
        self.name = unit_type.name
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
        elif isinstance(self.unit_type, GroundUnitType):
            pixmap = VEHICLE_BANNERS.get(self.unit_type.dcs_id)
        if pixmap is None:
            pixmap = AIRCRAFT_BANNERS.get("Missing")
        header.setPixmap(pixmap.scaled(header.width(), header.height()))
        self.layout.addWidget(header, 0, 0)

        self.gridLayout = QGridLayout()

        # Build the topmost details grid.
        self.details_grid = QFrame()
        self.details_grid_layout = QGridLayout()
        self.details_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.name_box = QLabel(
            f"<b>Name:</b> {unit_type.manufacturer} {unit_type.name}"
        )
        self.name_box.setProperty("style", "info-element")

        self.country_box = QLabel(
            f"<b>Country of Origin:</b> {unit_type.country_of_origin}"
        )
        self.country_box.setProperty("style", "info-element")

        self.role_box = QLabel(f"<b>Role:</b> {unit_type.role}")
        self.role_box.setProperty("style", "info-element")

        self.year_box = QLabel(
            f"<b>Variant Introduction:</b> {unit_type.year_introduced}"
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
            tasks = ", ".join(str(t) for t in unit_type.iter_task_capabilities())
            self.tasks_box = QLabel(f"<b>In-Game Tasks:</b> {tasks}")
            self.tasks_box.setProperty("style", "info-element")
            self.gridLayout.addWidget(self.tasks_box, 2, 0)

        # Finally, add the description box.
        self.details_text = QTextBrowser()
        self.details_text.setProperty("style", "info-desc")
        self.details_text.setText(unit_type.description)
        self.details_text.setOpenExternalLinks(
            True
        )  # in aircrafttype.py and groundunittype.py, for the descriptions, if No Data. including a google search link
        self.gridLayout.addWidget(self.details_text, 3, 0)

        self.layout.addLayout(self.gridLayout, 1, 0)
        self.setLayout(self.layout)
