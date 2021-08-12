from __future__ import annotations

import logging
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QGridLayout,
    QApplication,
)

from game.dcs.unittype import UnitType
from game.theater import ControlPoint
from game.unitdelivery import PendingUnitDeliveries
from qt_ui.models import GameModel
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QUnitInfoWindow import QUnitInfoWindow
from enum import Enum


class RecruitType(Enum):
    BUY = 0
    SELL = 1


class PurchaseGroup(QGroupBox):
    def __init__(self, unit_type: UnitType, recruiter: QRecruitBehaviour) -> None:
        super().__init__()
        self.unit_type = unit_type
        self.recruiter = recruiter

        self.setProperty("style", "buy-box")
        self.setMaximumHeight(36)
        self.setMinimumHeight(36)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.sell_button = QPushButton("-")
        self.sell_button.setProperty("style", "btn-sell")
        self.sell_button.setDisabled(not recruiter.enable_sale(unit_type))
        self.sell_button.setMinimumSize(16, 16)
        self.sell_button.setMaximumSize(16, 16)
        self.sell_button.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        )

        self.sell_button.clicked.connect(
            lambda: self.recruiter.recruit_handler(RecruitType.SELL, self.unit_type)
        )

        self.amount_bought = QLabel()
        self.amount_bought.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        )

        self.buy_button = QPushButton("+")
        self.buy_button.setProperty("style", "btn-buy")
        self.buy_button.setDisabled(not recruiter.enable_purchase(unit_type))
        self.buy_button.setMinimumSize(16, 16)
        self.buy_button.setMaximumSize(16, 16)

        self.buy_button.clicked.connect(
            lambda: self.recruiter.recruit_handler(RecruitType.BUY, self.unit_type)
        )
        self.buy_button.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        layout.addWidget(self.sell_button)
        layout.addWidget(self.amount_bought)
        layout.addWidget(self.buy_button)

        self.update_state()

    @property
    def pending_units(self) -> int:
        return self.recruiter.pending_deliveries.units.get(self.unit_type, 0)

    def update_state(self) -> None:
        self.buy_button.setEnabled(self.recruiter.enable_purchase(self.unit_type))
        self.buy_button.setToolTip(
            self.recruiter.purchase_tooltip(self.buy_button.isEnabled())
        )
        self.sell_button.setEnabled(self.recruiter.enable_sale(self.unit_type))
        self.sell_button.setToolTip(
            self.recruiter.sell_tooltip(self.sell_button.isEnabled())
        )
        self.amount_bought.setText(f"<b>{self.pending_units}</b>")


class QRecruitBehaviour:
    game_model: GameModel
    cp: ControlPoint
    purchase_groups: dict[UnitType, PurchaseGroup]
    existing_units_labels = None
    maximum_units = -1
    BUDGET_FORMAT = "Available Budget: <b>${:.2f}M</b>"

    def __init__(self) -> None:
        self.existing_units_labels = {}
        self.purchase_groups = {}
        self.update_available_budget()

    @property
    def pending_deliveries(self) -> PendingUnitDeliveries:
        return self.cp.pending_unit_deliveries

    @property
    def budget(self) -> float:
        return self.game_model.game.budget

    @budget.setter
    def budget(self, value: int) -> None:
        self.game_model.game.budget = value

    def add_purchase_row(
        self,
        unit_type: UnitType,
        layout: QGridLayout,
        row: int,
    ) -> None:
        exist = QGroupBox()
        exist.setProperty("style", "buy-box")
        exist.setMaximumHeight(36)
        exist.setMinimumHeight(36)
        existLayout = QHBoxLayout()
        exist.setLayout(existLayout)

        existing_units = self.cp.base.total_units_of_type(unit_type)

        unitName = QLabel(f"<b>{unit_type.name}</b>")
        unitName.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        existing_units = QLabel(str(existing_units))
        existing_units.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.existing_units_labels[unit_type] = existing_units

        price = QLabel(f"<b>$ {unit_type.price}</b> M")
        price.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        purchase_group = PurchaseGroup(unit_type, self)
        self.purchase_groups[unit_type] = purchase_group

        info = QGroupBox()
        info.setProperty("style", "buy-box")
        info.setMaximumHeight(36)
        info.setMinimumHeight(36)
        infolayout = QHBoxLayout()
        info.setLayout(infolayout)

        unitInfo = QPushButton("i")
        unitInfo.setProperty("style", "btn-info")
        unitInfo.setMinimumSize(16, 16)
        unitInfo.setMaximumSize(16, 16)
        unitInfo.clicked.connect(lambda: self.info(unit_type))
        unitInfo.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        existLayout.addWidget(unitName)
        existLayout.addItem(
            QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )
        existLayout.addWidget(existing_units)
        existLayout.addItem(
            QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )
        existLayout.addWidget(price)

        infolayout.addWidget(unitInfo)

        layout.addWidget(exist, row, 1)
        layout.addWidget(purchase_group, row, 2)
        layout.addWidget(info, row, 3)

    def update_available_budget(self) -> None:
        GameUpdateSignal.get_instance().updateBudget(self.game_model.game)

    def recruit_handler(self, recruit_type: RecruitType, unit_type: UnitType) -> None:
        # Lookup if Keyboard Modifiers were pressed
        # Shift = 10 times
        # CTRL = 5 Times
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            amount = 10
        elif modifiers == Qt.ControlModifier:
            amount = 5
        else:
            amount = 1

        for i in range(amount):
            if recruit_type == RecruitType.SELL:
                if not self.sell(unit_type):
                    return
            elif recruit_type == RecruitType.BUY:
                if not self.buy(unit_type):
                    return

    def buy(self, unit_type: UnitType) -> bool:

        if not self.enable_purchase(unit_type):
            logging.error(f"Purchase of {unit_type} not allowed at {self.cp.name}")
            return False

        self.pending_deliveries.order({unit_type: 1})
        self.budget -= unit_type.price
        self.update_purchase_controls()
        self.update_available_budget()
        return True

    def sell(self, unit_type: UnitType) -> bool:
        if self.pending_deliveries.available_next_turn(unit_type) > 0:
            self.budget += unit_type.price
            self.pending_deliveries.sell({unit_type: 1})
        self.update_purchase_controls()
        self.update_available_budget()
        return True

    def update_purchase_controls(self) -> None:
        for group in self.purchase_groups.values():
            group.update_state()

    def enable_purchase(self, unit_type: UnitType) -> bool:
        return self.budget >= unit_type.price

    def enable_sale(self, unit_type: UnitType) -> bool:
        return True

    def purchase_tooltip(self, is_enabled: bool) -> str:
        if is_enabled:
            return "Buy unit. Use Shift or Ctrl key to buy multiple units at once."
        else:
            return "Unit can not be bought."

    def sell_tooltip(self, is_enabled: bool) -> str:
        if is_enabled:
            return "Sell unit. Use Shift or Ctrl key to buy multiple units at once."
        else:
            return "Unit can not be sold."

    def info(self, unit_type: UnitType) -> None:
        self.info_window = QUnitInfoWindow(self.game_model.game, unit_type)
        self.info_window.show()

    def set_maximum_units(self, maximum_units):
        """
        Set the maximum number of units that can be bought
        """
        self.maximum_units = maximum_units
