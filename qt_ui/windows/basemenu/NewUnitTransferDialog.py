from __future__ import annotations

import logging
from collections import defaultdict
from typing import Callable, Dict, Type

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
from dcs.unittype import UnitType

from game import Game
from game.dcs.groundunittype import GroundUnitType
from game.theater import ControlPoint
from game.transfers import TransferOrder
from qt_ui.models import GameModel
from qt_ui.widgets.QLabeledWidget import QLabeledWidget


class TransferDestinationComboBox(QComboBox):
    def __init__(self, game: Game, origin: ControlPoint) -> None:
        super().__init__()
        self.game = game
        self.origin = origin

        for cp in self.game.theater.controlpoints:
            if (
                cp != self.origin
                and cp.is_friendly(to_player=True)
                and cp.can_deploy_ground_units
            ):
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

        units_column = sorted(cp.base.armor, key=lambda u: u.name)

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


class TransferOptionsPanel(QVBoxLayout):
    def __init__(self, game: Game, origin: ControlPoint) -> None:
        super().__init__()

        self.source_combo_box = TransferDestinationComboBox(game, origin)
        self.transport_type = QComboBox()
        self.transport_type.addItem("Auto", "auto")
        self.transport_type.addItem("Airlift", "airlift")
        self.addLayout(QLabeledWidget("Destination:", self.source_combo_box))
        self.addLayout(QLabeledWidget("Requested transport type:", self.transport_type))

    @property
    def changed(self):
        return self.source_combo_box.currentIndexChanged

    @property
    def current(self) -> ControlPoint:
        return self.source_combo_box.currentData()

    @property
    def request_airlift(self) -> bool:
        return self.transport_type.currentData() == "airlift"


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
    transfer_quantity_changed = Signal()

    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        super().__init__()
        self.cp = cp
        self.game_model = game_model
        self.transfers: Dict[Type[UnitType, int]] = defaultdict(int)

        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()

        unit_types = set(self.game_model.game.faction_for(player=True).ground_units)
        sorted_units = sorted(
            {u for u in unit_types if self.cp.base.total_units_of_type(u)},
            key=lambda u: u.name,
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
        unit_type: GroundUnitType,
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

        unit_name = QLabel(f"<b>{unit_type.name}</b>")
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

            self.transfers[unit_type] += 1
            origin_inventory -= 1
            controls.set_quantity(self.transfers[unit_type])
            origin_inventory_label.setText(str(origin_inventory))
            self.transfer_quantity_changed.emit()

        def decrease(controls: TransferControls):
            nonlocal origin_inventory
            nonlocal origin_inventory_label
            if not controls.quantity:
                return

            self.transfers[unit_type] -= 1
            origin_inventory += 1
            controls.set_quantity(self.transfers[unit_type])
            origin_inventory_label.setText(str(origin_inventory))
            self.transfer_quantity_changed.emit()

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

        self.dest_panel = TransferOptionsPanel(game_model.game, origin)
        layout.addLayout(self.dest_panel)

        self.transfer_panel = ScrollingUnitTransferGrid(origin, game_model)
        self.transfer_panel.transfer_quantity_changed.connect(
            self.on_transfer_quantity_changed
        )
        layout.addWidget(self.transfer_panel)

        self.submit_button = QPushButton("Create Transfer Order", parent=self)
        self.submit_button.clicked.connect(self.on_submit)
        self.submit_button.setProperty("style", "start-button")
        self.submit_button.setDisabled(True)
        layout.addWidget(self.submit_button)

    def on_submit(self) -> None:
        destination = self.dest_panel.current
        transfers = {}
        for unit_type, count in self.transfer_panel.transfers.items():
            if not count:
                continue

            logging.info(
                f"Transferring {count} {unit_type} from {self.origin} to "
                f"{destination}"
            )
            transfers[unit_type] = count

        transfer = TransferOrder(
            origin=self.origin,
            destination=destination,
            units=transfers,
            request_airflift=self.dest_panel.request_airlift,
        )
        self.game_model.transfer_model.new_transfer(transfer)
        self.close()

    def on_transfer_quantity_changed(self) -> None:
        has_transfer_items = any(self.transfer_panel.transfers.values())
        self.submit_button.setDisabled(not has_transfer_items)
