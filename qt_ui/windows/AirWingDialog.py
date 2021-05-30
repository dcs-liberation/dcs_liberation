from typing import Optional, Type

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
from game.squadrons import Squadron
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
        CP_COLUMN = 0
        UNIT_TYPE_COLUMN = 1
        FLIGHT_TYPE_COLUMN = 2
        TARGET_NAME_COLUMN = 3

        self.table.setSortingEnabled(False)
        self.table.clear()

        inventory_rows = self.get_data(only_unallocated)
        self.table.setRowCount(len(inventory_rows))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Base", "Type", "Flight Type", "Target"])

        for idx, inv_row in enumerate(inventory_rows):
            self.table.setItem(idx, CP_COLUMN, QTableWidgetItem(inv_row[CP_COLUMN]))
            self.table.setItem(
                idx, UNIT_TYPE_COLUMN, QTableWidgetItem(inv_row[UNIT_TYPE_COLUMN])
            )
            self.table.setItem(
                idx, FLIGHT_TYPE_COLUMN, QTableWidgetItem(inv_row[FLIGHT_TYPE_COLUMN])
            )
            self.table.setItem(
                idx, TARGET_NAME_COLUMN, QTableWidgetItem(inv_row[TARGET_NAME_COLUMN])
            )

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def get_data(self, only_unallocated: bool) -> list[list[str]]:
        game = self.game_model.game
        ato = game.blue_ato
        inventory_rows = []

        for cp in game.theater.controlpoints:
            if cp.captured:
                cp_name = cp.name

                # Allocated aircraft
                if not only_unallocated:
                    for package in ato.packages:
                        for flight in package.flights:
                            if flight.from_cp == cp:
                                unit_type_name = self.format_unit_type(flight.unit_type)
                                num_units = flight.count
                                flight_type = flight.flight_type.value
                                target = flight.package.target.name
                                for _ in range(0, num_units):
                                    inventory_rows.append(
                                        [cp_name, unit_type_name, flight_type, target]
                                    )

                # Unallocated aircraft
                inventory = game.aircraft_inventory.for_control_point(cp)
                for unit_type, num_units in inventory.all_aircraft:
                    unit_type_name = self.format_unit_type(unit_type)
                    for _ in range(0, num_units):
                        inventory_rows.append([cp_name, unit_type_name, "Idle", "None"])

        return inventory_rows

    def format_unit_type(self, aircraft: Type[FlyingType]) -> str:
        return db.unit_get_expanded_info(self.country, aircraft, "name")


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
