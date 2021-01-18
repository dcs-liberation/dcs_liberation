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
from dcs.unittype import UnitType
from qt_ui.uiconstants import AIRCRAFT_BANNERS

from game.game import Game
from game import db


class QUnitInfoWindow(QDialog):

    def __init__(self, game: Game, unit_type: Type[UnitType]) -> None:
        super(QUnitInfoWindow, self).__init__()
        self.setModal(True)
        self.game = game
        self.unit_type = unit_type
        self.setWindowTitle(f"Unit Info: {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'name')}")
        self.setWindowIcon(QIcon("./resources/icon.png"))
        self.setMinimumHeight(570)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 720, 360)
        pixmap = AIRCRAFT_BANNERS.get(self.unit_type.id)
        if pixmap is None:
            pixmap = AIRCRAFT_BANNERS.get("Missing")
        header.setPixmap(pixmap.scaled(header.width(), header.height()))
        self.layout.addWidget(header, 0, 0)

        self.gridLayout = QGridLayout()
        
        self.details_grid = QFrame()
        self.details_grid_layout = QGridLayout()

        self.name_box = QLabel(f"<b>Name:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'name')}")
        self.name_box.setProperty("style", "info-element")
        
        self.country_box = QLabel(f"<b>Country of Origin:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'country-of-origin')}")
        self.country_box.setProperty("style", "info-element")
        
        self.year_box = QLabel(f"<b>Variant Introduction:</b> {db.unit_get_expanded_info(self.game.player_country, self.unit_type, 'year-of-variant-introduction')}")
        self.year_box.setProperty("style", "info-element")
        
        self.details_grid_layout.addWidget(self.name_box, 0, 0)
        self.details_grid_layout.addWidget(self.country_box, 1, 0)
        self.details_grid_layout.addWidget(self.year_box, 2, 0)

        self.details_grid.setLayout(self.details_grid_layout)

        self.details_text = QTextBrowser()
        self.details_text.setProperty("style", "info-desc")
        self.details_text.setText(db.unit_get_expanded_info(self.game.player_country, self.unit_type, "text"))

        self.gridLayout.addWidget(self.details_grid, 1, 0)
        self.gridLayout.addWidget(self.details_text, 2, 0)

        self.layout.addLayout(self.gridLayout, 1, 0)
        self.setLayout(self.layout)