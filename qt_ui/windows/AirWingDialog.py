from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Type, Iterator

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    Qt,
    QSize,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDialog,
    QListView,
    QVBoxLayout,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)
from dcs.unittype import FlyingType

from game import db
from game.inventory import ControlPointAircraftInventory
from game.squadrons import Squadron
from gen.flights.flight import Flight
from qt_ui.delegates import TwoColumnRowDelegate
from qt_ui.models import GameModel, AirWingModel, SquadronModel
from qt_ui.windows.SquadronDialog import SquadronDialog


class SquadronDelegate(TwoColumnRowDelegate):
    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__(rows=2, columns=2, font_size=12)
        self.air_wing_model = air_wing_model

    @staticmethod
    def squadron(index: QModelIndex) -> Squadron:
        return index.data(AirWingModel.SquadronRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        if (row, column) == (0, 0):
            return self.air_wing_model.data(index, Qt.DisplayRole)
        elif (row, column) == (0, 1):
            squadron = self.air_wing_model.data(index, AirWingModel.SquadronRole)
            return db.unit_get_expanded_info(
                squadron.country, squadron.aircraft, "name"
            )
        elif (row, column) == (1, 0):
            return self.squadron(index).nickname
        elif (row, column) == (1, 1):
            squadron = self.squadron(index)
            active = len(squadron.active_pilots)
            available = len(squadron.available_pilots)
            return f"{squadron.size} pilots, {active} active, {available} unassigned"
        return ""


class SquadronList(QListView):
    """List view for displaying the air wing's squadrons."""

    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__()
        self.air_wing_model = air_wing_model
        self.dialog: Optional[SquadronDialog] = None

        self.setIconSize(QSize(91, 24))
        self.setItemDelegate(SquadronDelegate(self.air_wing_model))
        self.setModel(self.air_wing_model)
        self.selectionModel().setCurrentIndex(
            self.air_wing_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )

        # self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.dialog = SquadronDialog(
            SquadronModel(self.air_wing_model.squadron_at_index(index)), self
        )
        self.dialog.show()


@dataclass(frozen=True)
class AircraftInventoryData:
    location: str
    unit_type: str
    task: str
    target: str
    pilot: str
    player: str

    @classmethod
    def headers(cls) -> list[str]:
        return ["Base", "Type", "Flight Type", "Target", "Pilot", "Player"]

    @property
    def columns(self) -> Iterator[str]:
        yield self.location
        yield self.unit_type
        yield self.task
        yield self.target
        yield self.pilot
        yield self.player

    @classmethod
    def from_flight(cls, flight: Flight) -> Iterator[AircraftInventoryData]:
        unit_type_name = cls.format_unit_type(flight.unit_type, flight.country)
        num_units = flight.count
        flight_type = flight.flight_type.value
        target = flight.package.target.name
        for idx in range(0, num_units):
            pilot = flight.pilots[idx]
            if pilot is None:
                pilot_name = "Unassigned"
                player = ""
            else:
                pilot_name = pilot.name
                player = "Player" if pilot.player else "AI"
            yield AircraftInventoryData(
                flight.departure.name,
                unit_type_name,
                flight_type,
                target,
                pilot_name,
                player,
            )

    @classmethod
    def each_from_inventory(
        cls, inventory: ControlPointAircraftInventory, country: str
    ) -> Iterator[AircraftInventoryData]:
        for unit_type, num_units in inventory.all_aircraft:
            unit_type_name = cls.format_unit_type(unit_type, country)
            for _ in range(0, num_units):
                yield AircraftInventoryData(
                    inventory.control_point.name,
                    unit_type_name,
                    "Idle",
                    "N/A",
                    "N/A",
                    "N/A",
                )

    @staticmethod
    def format_unit_type(aircraft: Type[FlyingType], country: str) -> str:
        return db.unit_get_expanded_info(country, aircraft, "name")


class AirInventoryView(QWidget):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__()

        self.game_model = game_model
        self.country = self.game_model.game.country_for(player=True)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.only_unallocated_cb = QCheckBox("Unallocated Only?")
        self.only_unallocated_cb.toggled.connect(self.update_table)

        layout.addWidget(self.only_unallocated_cb)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.update_table(False)

    def update_table(self, only_unallocated: bool) -> None:
        self.table.setSortingEnabled(False)
        self.table.clear()

        inventory_rows = list(self.get_data(only_unallocated))
        self.table.setRowCount(len(inventory_rows))
        headers = AircraftInventoryData.headers()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for row, data in enumerate(inventory_rows):
            for column, value in enumerate(data.columns):
                self.table.setItem(row, column, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def iter_allocated_aircraft(self) -> Iterator[AircraftInventoryData]:
        for package in self.game_model.game.blue_ato.packages:
            for flight in package.flights:
                yield from AircraftInventoryData.from_flight(flight)

    def iter_unallocated_aircraft(self) -> Iterator[AircraftInventoryData]:
        game = self.game_model.game
        for control_point, inventory in game.aircraft_inventory.inventories.items():
            if control_point.captured:
                yield from AircraftInventoryData.each_from_inventory(
                    inventory, game.country_for(player=True)
                )

    def get_data(self, only_unallocated: bool) -> Iterator[AircraftInventoryData]:
        yield from self.iter_unallocated_aircraft()
        if not only_unallocated:
            yield from self.iter_allocated_aircraft()


class AirWingTabs(QTabWidget):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__()

        self.addTab(SquadronList(game_model.blue_air_wing_model), "Squadrons")
        self.addTab(AirInventoryView(game_model), "Inventory")


class AirWingDialog(QDialog):
    """Dialog window showing the player's air wing."""

    def __init__(self, game_model: GameModel, parent) -> None:
        super().__init__(parent)
        self.air_wing_model = game_model.blue_air_wing_model

        self.setMinimumSize(1000, 440)
        self.setWindowTitle(f"Air Wing")
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(AirWingTabs(game_model))
