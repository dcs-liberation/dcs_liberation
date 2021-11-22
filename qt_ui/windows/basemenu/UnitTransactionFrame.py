from __future__ import annotations

import logging
from enum import Enum
from typing import Generic, TypeVar

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)

from game.purchaseadapter import PurchaseAdapter, TransactionError
from qt_ui.models import GameModel
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QUnitInfoWindow import QUnitInfoWindow


class RecruitType(Enum):
    BUY = 0
    SELL = 1


TransactionItemType = TypeVar("TransactionItemType")


class PurchaseGroup(QGroupBox, Generic[TransactionItemType]):
    def __init__(
        self,
        item: TransactionItemType,
        recruiter: UnitTransactionFrame[TransactionItemType],
    ) -> None:
        super().__init__()
        self.item = item
        self.recruiter = recruiter

        self.setProperty("style", "buy-box")
        self.setMaximumHeight(72)
        self.setMinimumHeight(36)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.sell_button = QPushButton("-")
        self.sell_button.setProperty("style", "btn-sell")
        self.sell_button.setDisabled(not recruiter.enable_sale(item))
        self.sell_button.setMinimumSize(16, 16)
        self.sell_button.setMaximumSize(16, 16)
        self.sell_button.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        )

        self.sell_button.clicked.connect(
            lambda: self.recruiter.recruit_handler(RecruitType.SELL, self.item)
        )

        self.amount_bought = QLabel()
        self.amount_bought.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        )

        self.buy_button = QPushButton("+")
        self.buy_button.setProperty("style", "btn-buy")
        self.buy_button.setDisabled(not recruiter.enable_purchase(item))
        self.buy_button.setMinimumSize(16, 16)
        self.buy_button.setMaximumSize(16, 16)

        self.buy_button.clicked.connect(
            lambda: self.recruiter.recruit_handler(RecruitType.BUY, self.item)
        )
        self.buy_button.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        layout.addWidget(self.sell_button)
        layout.addWidget(self.amount_bought)
        layout.addWidget(self.buy_button)

        self.update_state()

    @property
    def pending_units(self) -> int:
        return self.recruiter.pending_delivery_quantity(self.item)

    def update_state(self) -> None:
        self.buy_button.setEnabled(self.recruiter.enable_purchase(self.item))
        self.buy_button.setToolTip(
            self.recruiter.purchase_tooltip(self.buy_button.isEnabled())
        )
        self.sell_button.setEnabled(self.recruiter.enable_sale(self.item))
        self.sell_button.setToolTip(
            self.recruiter.sell_tooltip(self.sell_button.isEnabled())
        )
        self.amount_bought.setText(f"<b>{self.pending_units}</b>")


class UnitTransactionFrame(QFrame, Generic[TransactionItemType]):
    BUDGET_FORMAT = "Available Budget: <b>${:.2f}M</b>"

    def __init__(
        self,
        game_model: GameModel,
        purchase_adapter: PurchaseAdapter[TransactionItemType],
    ) -> None:
        super().__init__()
        self.game_model = game_model
        self.purchase_adapter = purchase_adapter
        self.existing_units_labels = {}
        self.purchase_groups: dict[
            TransactionItemType, PurchaseGroup[TransactionItemType]
        ] = {}
        self.update_available_budget()

    def current_quantity_of(self, item: TransactionItemType) -> int:
        return self.purchase_adapter.current_quantity_of(item)

    def pending_delivery_quantity(self, item: TransactionItemType) -> int:
        return self.purchase_adapter.pending_delivery_quantity(item)

    def expected_quantity_next_turn(self, item: TransactionItemType) -> int:
        return self.purchase_adapter.expected_quantity_next_turn(item)

    def display_name_of(
        self, item: TransactionItemType, multiline: bool = False
    ) -> str:
        return self.purchase_adapter.name_of(item, multiline)

    def price_of(self, item: TransactionItemType) -> int:
        return self.purchase_adapter.price_of(item)

    @property
    def budget(self) -> float:
        return self.game_model.game.blue.budget

    @budget.setter
    def budget(self, value: int) -> None:
        self.game_model.game.blue.budget = value

    def add_purchase_row(
        self,
        item: TransactionItemType,
        layout: QGridLayout,
        row: int,
    ) -> None:
        exist = QGroupBox()
        exist.setProperty("style", "buy-box")
        exist.setMaximumHeight(72)
        exist.setMinimumHeight(36)
        existLayout = QHBoxLayout()
        existLayout.setSizeConstraint(QLayout.SetMinimumSize)
        exist.setLayout(existLayout)

        existing_units = self.current_quantity_of(item)

        unitName = QLabel(f"<b>{self.display_name_of(item, multiline=True)}</b>")
        unitName.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        existing_units = QLabel(str(existing_units))
        existing_units.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.existing_units_labels[item] = existing_units

        price = QLabel(f"<b>$ {self.price_of(item)}</b> M")
        price.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        purchase_group = PurchaseGroup(item, self)
        self.purchase_groups[item] = purchase_group

        info = QGroupBox()
        info.setProperty("style", "buy-box")
        info.setMaximumHeight(72)
        info.setMinimumHeight(36)
        infolayout = QHBoxLayout()
        info.setLayout(infolayout)

        unitInfo = QPushButton("i")
        unitInfo.setProperty("style", "btn-info")
        unitInfo.setMinimumSize(16, 16)
        unitInfo.setMaximumSize(16, 16)
        unitInfo.clicked.connect(lambda: self.info(item))
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

    def recruit_handler(
        self, recruit_type: RecruitType, item: TransactionItemType
    ) -> None:
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

        if recruit_type == RecruitType.SELL:
            self.sell(item, amount)
        elif recruit_type == RecruitType.BUY:
            self.buy(item, amount)

    def post_transaction_update(self) -> None:
        self.update_purchase_controls()
        self.update_available_budget()

    def buy(self, item: TransactionItemType, quantity: int) -> None:
        try:
            self.purchase_adapter.buy(item, quantity)
        except TransactionError as ex:
            logging.exception(f"Purchase of {self.display_name_of(item)} failed")
            QMessageBox.warning(self, "Purchase failed", str(ex), QMessageBox.Ok)
        finally:
            self.post_transaction_update()

    def sell(self, item: TransactionItemType, quantity: int) -> None:
        try:
            self.purchase_adapter.sell(item, quantity)
        except TransactionError as ex:
            logging.exception(f"Sale of {self.display_name_of(item)} failed")
            QMessageBox.warning(self, "Sale failed", str(ex), QMessageBox.Ok)
        finally:
            self.post_transaction_update()

    def update_purchase_controls(self) -> None:
        for group in self.purchase_groups.values():
            group.update_state()

    def enable_purchase(self, item: TransactionItemType) -> bool:
        return self.purchase_adapter.can_buy(item)

    def enable_sale(self, item: TransactionItemType) -> bool:
        return self.purchase_adapter.can_sell_or_cancel(item)

    @staticmethod
    def purchase_tooltip(is_enabled: bool) -> str:
        if is_enabled:
            return "Buy unit. Use Shift or Ctrl key to buy multiple units at once."
        else:
            return "Unit can not be bought."

    @staticmethod
    def sell_tooltip(is_enabled: bool) -> str:
        if is_enabled:
            return "Sell unit. Use Shift or Ctrl key to buy multiple units at once."
        else:
            return "Unit can not be sold."

    def info(self, item: TransactionItemType) -> None:
        self.info_window = QUnitInfoWindow(
            self.game_model.game, self.purchase_adapter.unit_type_of(item)
        )
        self.info_window.show()
