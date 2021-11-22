from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Iterator

from PySide2.QtCore import QItemSelectionModel, QModelIndex, QSize
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
    QHBoxLayout,
)

from game.squadrons import Squadron
from game.theater import ConflictTheater
from game.ato.flight import Flight
from qt_ui.delegates import TwoColumnRowDelegate
from qt_ui.models import GameModel, AirWingModel, SquadronModel, AtoModel
from qt_ui.windows.SquadronDialog import SquadronDialog


class SquadronDelegate(TwoColumnRowDelegate):
    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__(rows=2, columns=2, font_size=12)
        self.air_wing_model = air_wing_model

    @staticmethod
    def squadron(index: QModelIndex) -> Squadron:
        return index.data(AirWingModel.SquadronRole)

    def text_for(self, index: QModelIndex, row: int, column: int) -> str:
        squadron = self.squadron(index)
        if (row, column) == (0, 0):
            if squadron.nickname:
                nickname = f' "{squadron.nickname}"'
            else:
                nickname = ""
            return f"{squadron.name}{nickname}"
        elif (row, column) == (0, 1):
            return squadron.aircraft.name
        elif (row, column) == (1, 0):
            return squadron.location.name
        elif (row, column) == (1, 1):
            squadron = self.squadron(index)
            active = len(squadron.active_pilots)
            available = len(squadron.available_pilots)
            on_leave = len(squadron.pilots_on_leave)
            return f"{active} active, {available} unassigned, {on_leave} on leave"
        return ""


class SquadronList(QListView):
    """List view for displaying the air wing's squadrons."""

    def __init__(
        self,
        ato_model: AtoModel,
        air_wing_model: AirWingModel,
        theater: ConflictTheater,
    ) -> None:
        super().__init__()
        self.ato_model = ato_model
        self.air_wing_model = air_wing_model
        self.theater = theater
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
            self.ato_model,
            SquadronModel(self.air_wing_model.squadron_at_index(index)),
            self.theater,
            self,
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
        num_units = flight.count
        flight_type = flight.flight_type.value
        target = flight.package.target.name
        for idx in range(0, num_units):
            pilot = flight.roster.pilots[idx]
            if pilot is None:
                pilot_name = "Unassigned"
                player = ""
            else:
                pilot_name = pilot.name
                player = "Player" if pilot.player else "AI"
            yield AircraftInventoryData(
                flight.departure.name,
                flight.unit_type.name,
                flight_type,
                target,
                pilot_name,
                player,
            )

    @classmethod
    def each_untasked_from_squadron(
        cls, squadron: Squadron
    ) -> Iterator[AircraftInventoryData]:
        for _ in range(0, squadron.untasked_aircraft):
            yield AircraftInventoryData(
                squadron.name, squadron.aircraft.name, "Idle", "N/A", "N/A", "N/A"
            )


class AirInventoryView(QWidget):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__()
        self.game_model = game_model

        self.only_unallocated = False
        self.enemy_info = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        checkbox_row = QHBoxLayout()
        layout.addLayout(checkbox_row)

        self.only_unallocated_cb = QCheckBox("Unallocated only")
        self.only_unallocated_cb.toggled.connect(self.set_only_unallocated)
        checkbox_row.addWidget(self.only_unallocated_cb)

        self.enemy_info_cb = QCheckBox("Show enemy info")
        self.enemy_info_cb.toggled.connect(self.set_enemy_info)
        checkbox_row.addWidget(self.enemy_info_cb)

        checkbox_row.addStretch()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.set_only_unallocated(False)

    def set_only_unallocated(self, value: bool) -> None:
        self.only_unallocated = value
        self.update_table()

    def set_enemy_info(self, value: bool) -> None:
        self.enemy_info = value
        self.update_table()

    def update_table(self) -> None:
        self.table.setSortingEnabled(False)
        self.table.clear()

        inventory_rows = list(self.get_data())
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
        coalition = self.game_model.game.coalition_for(not self.enemy_info)
        for package in coalition.ato.packages:
            for flight in package.flights:
                yield from AircraftInventoryData.from_flight(flight)

    def iter_unallocated_aircraft(self) -> Iterator[AircraftInventoryData]:
        coalition = self.game_model.game.coalition_for(not self.enemy_info)
        for squadron in coalition.air_wing.iter_squadrons():
            yield from AircraftInventoryData.each_untasked_from_squadron(squadron)

    def get_data(self) -> Iterator[AircraftInventoryData]:
        yield from self.iter_unallocated_aircraft()
        if not self.only_unallocated:
            yield from self.iter_allocated_aircraft()


class AirWingTabs(QTabWidget):
    def __init__(self, game_model: GameModel) -> None:
        super().__init__()

        self.addTab(
            SquadronList(
                game_model.ato_model,
                game_model.blue_air_wing_model,
                game_model.game.theater,
            ),
            "Squadrons",
        )
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
