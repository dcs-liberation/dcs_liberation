from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, Type

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
from dcs.task import PinpointStrike
from dcs.unittype import FlyingType, UnitType, VehicleType

from game import Game, db
from game.inventory import ControlPointAircraftInventory
from game.theater import ControlPoint, SupplyRoute
from game.transfers import AirliftOrder, RoadTransferOrder
from gen.ato import Package
from gen.flights.flight import Flight, FlightType
from gen.flights.flightplan import FlightPlanBuilder, PlanningError
from qt_ui.models import GameModel, PackageModel
from qt_ui.widgets.QLabeledWidget import QLabeledWidget


class TransferDestinationComboBox(QComboBox):
    def __init__(self, origin: ControlPoint) -> None:
        super().__init__()

        for cp in SupplyRoute.for_control_point(origin):
            if cp != origin and cp.captured:
                self.addItem(cp.name, cp)
        self.model().sort(0)
        self.setCurrentIndex(0)


class UnitTransferList(QFrame):
    def __init__(self, cp: ControlPoint, game_model: GameModel):
        super().__init__(self)
        self.cp = cp
        self.game_model = game_model

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        scroll_content.setLayout(task_box_layout)

        units_column = sorted(
            cp.base.armor,
            key=lambda u: db.unit_get_expanded_info(
                self.game_model.game.player_country, u, "name"
            ),
        )

        count = 0
        for count, unit_type in enumerate(units_column):
            self.add_purchase_row(unit_type, task_box_layout, count)
        stretch = QVBoxLayout()
        stretch.addStretch()
        task_box_layout.addLayout(stretch, count, 0)

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)


@dataclass(frozen=True)
class AirliftCapacity:
    helicopter: int
    cargo_plane: int

    @property
    def total(self) -> int:
        return self.helicopter + self.cargo_plane

    @classmethod
    def to_control_point(cls, game: Game) -> AirliftCapacity:
        helo_capacity = 0
        plane_capacity = 0
        for cp in game.theater.player_points():
            inventory = game.aircraft_inventory.for_control_point(cp)
            for unit_type, count in inventory.all_aircraft:
                if unit_type.helicopter:
                    helo_capacity += count
        return AirliftCapacity(helicopter=helo_capacity, cargo_plane=plane_capacity)


class TransferOptionsPanel(QVBoxLayout):
    def __init__(self, origin: ControlPoint, airlift_capacity: AirliftCapacity) -> None:
        super().__init__()

        self.source_combo_box = TransferDestinationComboBox(origin)
        self.addLayout(QLabeledWidget("Destination:", self.source_combo_box))
        self.airlift = QCheckBox()
        self.airlift.toggled.connect(self.set_airlift)
        self.addLayout(QLabeledWidget("Airlift (WIP):", self.airlift))
        self.addWidget(
            QLabel(
                f"{airlift_capacity.total} airlift capacity "
                f"({airlift_capacity.cargo_plane} from cargo planes, "
                f"{airlift_capacity.helicopter} from helicopters)"
            )
        )

    @property
    def changed(self):
        return self.source_combo_box.currentIndexChanged

    @property
    def current(self) -> ControlPoint:
        return self.source_combo_box.currentData()

    def set_airlift(self, value: bool) -> None:
        pass


class TransferControls(QGroupBox):
    def __init__(
        self,
        increase_text: str,
        on_increase: Callable[[TransferControls], None],
        decrease_text: str,
        on_decrease: Callable[[TransferControls], None],
        initial_amount: int = 0,
        disabled: bool = False,
    ) -> None:
        super().__init__()

        self.quantity = initial_amount

        self.setProperty("style", "buy-box")
        self.setMaximumHeight(36)
        self.setMinimumHeight(36)
        layout = QHBoxLayout()
        self.setLayout(layout)

        decrease = QPushButton(decrease_text)
        decrease.setProperty("style", "btn-sell")
        decrease.setDisabled(disabled)
        decrease.setMinimumSize(16, 16)
        decrease.setMaximumSize(16, 16)
        decrease.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        decrease.clicked.connect(lambda: on_decrease(self))
        layout.addWidget(decrease)

        self.count_label = QLabel()
        self.count_label.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        )
        self.set_quantity(initial_amount)
        layout.addWidget(self.count_label)

        increase = QPushButton(increase_text)
        increase.setProperty("style", "btn-buy")
        increase.setDisabled(disabled)
        increase.setMinimumSize(16, 16)
        increase.setMaximumSize(16, 16)
        increase.clicked.connect(lambda: on_increase(self))
        increase.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        layout.addWidget(increase)

    def set_quantity(self, quantity: int) -> None:
        self.quantity = quantity
        self.count_label.setText(f"<b>{self.quantity}</b>")


class ScrollingUnitTransferGrid(QFrame):
    def __init__(
        self,
        cp: ControlPoint,
        airlift: bool,
        airlift_capacity: AirliftCapacity,
        game_model: GameModel,
    ) -> None:
        super().__init__()
        self.cp = cp
        self.airlift = airlift
        self.remaining_capacity = airlift_capacity.total
        self.game_model = game_model
        self.transfers: Dict[Type[UnitType, int]] = defaultdict(int)

        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()

        unit_types = set(
            db.find_unittype(PinpointStrike, self.game_model.game.player_name)
        )
        sorted_units = sorted(
            {u for u in unit_types if self.cp.base.total_units_of_type(u)},
            key=lambda u: db.unit_get_expanded_info(
                self.game_model.game.player_country, u, "name"
            ),
        )
        for row, unit_type in enumerate(sorted_units):
            self.add_unit_row(unit_type, task_box_layout, row)
        stretch = QVBoxLayout()
        stretch.addStretch()
        task_box_layout.addLayout(stretch, task_box_layout.count(), 0)

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def add_unit_row(
        self,
        unit_type: Type[UnitType],
        layout: QGridLayout,
        row: int,
    ) -> None:
        exist = QGroupBox()
        exist.setProperty("style", "buy-box")
        exist.setMaximumHeight(36)
        exist.setMinimumHeight(36)
        origin_inventory_layout = QHBoxLayout()
        exist.setLayout(origin_inventory_layout)

        origin_inventory = self.cp.base.total_units_of_type(unit_type)

        unit_name = QLabel(
            "<b>"
            + db.unit_get_expanded_info(
                self.game_model.game.player_country, unit_type, "name"
            )
            + "</b>"
        )
        unit_name.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        origin_inventory_label = QLabel(str(origin_inventory))
        origin_inventory_label.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        )

        def increase(controls: TransferControls):
            nonlocal origin_inventory
            nonlocal origin_inventory_label
            if not origin_inventory:
                return

            if self.airlift:
                if not self.remaining_capacity:
                    return
                self.remaining_capacity -= 1

            self.transfers[unit_type] += 1
            origin_inventory -= 1
            controls.set_quantity(self.transfers[unit_type])
            origin_inventory_label.setText(str(origin_inventory))

        def decrease(controls: TransferControls):
            nonlocal origin_inventory
            nonlocal origin_inventory_label
            if not controls.quantity:
                return

            if self.airlift:
                self.remaining_capacity += 1

            self.transfers[unit_type] -= 1
            origin_inventory += 1
            controls.set_quantity(self.transfers[unit_type])
            origin_inventory_label.setText(str(origin_inventory))

        transfer_controls = TransferControls("->", increase, "<-", decrease)

        origin_inventory_layout.addWidget(unit_name)
        origin_inventory_layout.addItem(
            QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )
        origin_inventory_layout.addWidget(origin_inventory_label)
        origin_inventory_layout.addItem(
            QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )

        layout.addWidget(exist, row, 1)
        layout.addWidget(transfer_controls, row, 2)


class NewUnitTransferDialog(QDialog):
    def __init__(
        self,
        game_model: GameModel,
        origin: ControlPoint,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.origin = origin
        self.setWindowTitle(f"New unit transfer from {origin.name}")

        self.game_model = game_model

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.airlift_capacity = AirliftCapacity.to_control_point(game_model.game)
        self.dest_panel = TransferOptionsPanel(origin, self.airlift_capacity)
        self.dest_panel.changed.connect(self.rebuild_transfers)
        layout.addLayout(self.dest_panel)

        self.transfer_panel = ScrollingUnitTransferGrid(
            origin,
            airlift=False,
            airlift_capacity=self.airlift_capacity,
            game_model=game_model,
        )
        self.dest_panel.airlift.toggled.connect(self.rebuild_transfers)
        layout.addWidget(self.transfer_panel)

        self.submit_button = QPushButton("Create Transfer Order", parent=self)
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setProperty("style", "start-button")
        layout.addWidget(self.submit_button)

    def rebuild_transfers(self) -> None:
        # Rebuild the transfer panel to reset everything. It's easier to recreate the
        # panel itself than to clear the grid layout in the panel.
        self.layout().removeWidget(self.transfer_panel)
        self.layout().removeWidget(self.submit_button)
        self.transfer_panel = ScrollingUnitTransferGrid(
            self.origin,
            airlift=self.dest_panel.airlift.isChecked(),
            airlift_capacity=self.airlift_capacity,
            game_model=self.game_model,
        )
        self.layout().addWidget(self.transfer_panel)
        self.layout().addWidget(self.submit_button)

    def on_submit(self) -> None:
        transfers = {}
        for unit_type, count in self.transfer_panel.transfers.items():
            if not count:
                continue

            logging.info(
                f"Transferring {count} {unit_type.id} from "
                f"{self.transfer_panel.cp.name} to {self.dest_panel.current.name}"
            )
            transfers[unit_type] = count

        if self.dest_panel.airlift.isChecked():
            self.create_package_for_airlift(
                self.transfer_panel.cp,
                self.dest_panel.current,
                transfers,
            )
        else:
            transfer = RoadTransferOrder(
                player=True,
                origin=self.transfer_panel.cp,
                destination=self.dest_panel.current,
                units=transfers,
            )
            self.game_model.transfer_model.new_transfer(transfer)
        self.close()

    @staticmethod
    def take_units(
        units: Dict[Type[VehicleType], int], count: int
    ) -> Dict[Type[VehicleType], int]:
        taken = {}
        for unit_type, remaining in units.items():
            take = min(remaining, count)
            count -= take
            units[unit_type] -= take
            taken[unit_type] = take
            if not count:
                break
        return taken

    def create_airlift_flight(
        self,
        game: Game,
        package_model: PackageModel,
        unit_type: Type[FlyingType],
        inventory: ControlPointAircraftInventory,
        needed_capacity: int,
        pickup: ControlPoint,
        drop_off: ControlPoint,
        units: Dict[Type[VehicleType], int],
    ) -> int:
        available = inventory.available(unit_type)
        # 4 is the max flight size in DCS.
        flight_size = min(needed_capacity, available, 4)
        flight = Flight(
            package_model.package,
            game.player_country,
            unit_type,
            flight_size,
            FlightType.TRANSPORT,
            game.settings.default_start_type,
            departure=inventory.control_point,
            arrival=inventory.control_point,
            divert=None,
        )

        transfer = AirliftOrder(
            player=True,
            origin=pickup,
            destination=drop_off,
            units=self.take_units(units, flight_size),
            flight=flight,
        )
        flight.cargo = transfer

        package_model.add_flight(flight)
        planner = FlightPlanBuilder(game, package_model.package, is_player=True)
        try:
            planner.populate_flight_plan(flight)
        except PlanningError as ex:
            package_model.delete_flight(flight)
            logging.exception("Could not create flight")
            QMessageBox.critical(
                self, "Could not create flight", str(ex), QMessageBox.Ok
            )
        game.aircraft_inventory.claim_for_flight(flight)
        self.game_model.transfer_model.new_transfer(transfer)
        return flight_size

    def create_package_for_airlift(
        self,
        pickup: ControlPoint,
        drop_off: ControlPoint,
        units: Dict[Type[VehicleType], int],
    ) -> None:
        package = Package(target=drop_off, auto_asap=True)
        package_model = PackageModel(package, self.game_model)

        needed_capacity = sum(c for c in units.values())
        game = self.game_model.game
        for cp in game.theater.player_points():
            inventory = game.aircraft_inventory.for_control_point(cp)
            for unit_type, available in inventory.all_aircraft:
                if unit_type.helicopter:
                    while available and needed_capacity:
                        flight_size = self.create_airlift_flight(
                            self.game_model.game,
                            package_model,
                            unit_type,
                            inventory,
                            needed_capacity,
                            pickup,
                            drop_off,
                            units,
                        )
                        available -= flight_size
                        needed_capacity -= flight_size
        package_model.update_tot()
        self.game_model.ato_model.add_package(package)
