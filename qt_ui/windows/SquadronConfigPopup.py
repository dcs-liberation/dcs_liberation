from typing import Optional, Callable, Iterable

from PySide2.QtWidgets import (
    QDialog,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QHBoxLayout,
    QComboBox,
)

from game.dcs.aircrafttype import AircraftType
from game.game import Game
from game.squadrons import Squadron
from game.theater import ConflictTheater, ControlPoint
from game.coalition import Coalition
from game.factions.faction import Faction
from game.campaignloader.squadrondefgenerator import SquadronDefGenerator

from gen.flights.flight import FlightType


class AircraftTypeSelector(QComboBox):
    def __init__(self, faction: Faction) -> None:
        super().__init__()
        self.types = faction.aircrafts
        self.setSizeAdjustPolicy(self.AdjustToContents)

        self.addItem("Select aircraft type...", None)
        self.setCurrentText("Select aircraft type...")
        self.types.sort(key=str)

        for type in self.types:
            self.addItem(type.name, type)


class SquadronConfigPopup(QDialog):
    def __init__(
        self, coalition: Coalition, theater: ConflictTheater, game: Game
    ) -> None:
        super().__init__()
        self.game = game
        self.coalition = coalition
        self.theater = theater
        self.squadron = None

        # self.setMinimumSize(500, 800)
        self.setWindowTitle(f"Add new Squadron")

        self.column = QVBoxLayout()
        self.setLayout(self.column)

        self.aircraft_type_selector = AircraftTypeSelector(coalition.faction)
        self.column.addWidget(self.aircraft_type_selector)

        self.column.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit("---")
        self.name_edit.setEnabled(False)
        self.name_edit.textChanged.connect(self.on_name_changed)
        self.column.addWidget(self.name_edit)

        self.column.addWidget(QLabel("Nickname:"))
        self.nickname_edit = QLineEdit("---")
        self.nickname_edit.setEnabled(False)
        self.nickname_edit.textChanged.connect(self.on_nickname_changed)
        self.column.addWidget(self.nickname_edit)

        self.column.addStretch()
        self.aircraft_type_selector.currentIndexChanged.connect(
            self.on_aircraft_selection
        )

        self.button_layout = QHBoxLayout()
        self.column.addLayout(self.button_layout)

        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(lambda state: self.accept())
        self.accept_button.setEnabled(False)
        self.button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda state: self.cancel())
        self.button_layout.addWidget(self.cancel_button)

    def create_Squadron(
        self, aircraft_type: AircraftType, base: ControlPoint
    ) -> Squadron:
        squadron_def = SquadronDefGenerator(self.coalition).generate_for_aircraft(
            aircraft_type
        )
        squadron = Squadron(
            squadron_def.name,
            squadron_def.nickname,
            squadron_def.country,
            squadron_def.role,
            squadron_def.aircraft,
            squadron_def.livery,
            squadron_def.mission_types,
            squadron_def.operating_bases,
            squadron_def.pilot_pool,
            self.coalition,
            self.game.settings,
            base,
        )
        return squadron

    def on_aircraft_selection(self, index: int) -> None:
        aircraft_type_name = self.aircraft_type_selector.currentText()
        aircraft_type = None
        for aircraft in self.coalition.faction.aircrafts:
            if str(aircraft) == aircraft_type_name:
                aircraft_type = aircraft

        if aircraft != None:
            self.squadron = self.create_Squadron(
                aircraft_type,
                next(self.theater.control_points_for(self.coalition.player)),
            )

            self.name_edit.setText(self.squadron.name)
            self.name_edit.setEnabled(True)

            self.nickname_edit.setText(self.squadron.nickname)
            self.nickname_edit.setEnabled(True)

            self.accept_button.setStyleSheet("background-color: green")
            self.accept_button.setEnabled(True)

            self.update()

    def on_name_changed(self, text: str) -> None:
        self.squadron.name = text

    def on_nickname_changed(self, text: str) -> None:
        self.squadron.nickname = text

    def accept(self) -> None:
        self.coalition.air_wing.add_squadron(self.squadron)
        return super().accept()

    def cancel(self) -> None:
        return super().reject()
