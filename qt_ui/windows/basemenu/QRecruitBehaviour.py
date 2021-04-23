import logging
from typing import Type

from PySide2.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
from dcs.unittype import UnitType

from game import db
from game.theater import ControlPoint
from game.unitdelivery import PendingUnitDeliveries
from qt_ui.models import GameModel
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QUnitInfoWindow import QUnitInfoWindow


class QRecruitBehaviour:
    game_model: GameModel
    cp: ControlPoint
    existing_units_labels = None
    bought_amount_labels = None
    maximum_units = -1
    BUDGET_FORMAT = "Available Budget: <b>${:.2f}M</b>"

    def __init__(self) -> None:
        self.bought_amount_labels = {}
        self.existing_units_labels = {}
        self.update_available_budget()

    @property
    def pending_deliveries(self) -> PendingUnitDeliveries:
        return self.cp.pending_unit_deliveries

    @property
    def budget(self) -> int:
        return self.game_model.game.budget

    @budget.setter
    def budget(self, value: int) -> None:
        self.game_model.game.budget = value

    def add_purchase_row(
        self,
        unit_type: Type[UnitType],
        layout: QLayout,
        row: int,
    ) -> int:
        exist = QGroupBox()
        exist.setProperty("style", "buy-box")
        exist.setMaximumHeight(36)
        exist.setMinimumHeight(36)
        existLayout = QHBoxLayout()
        exist.setLayout(existLayout)

        existing_units = self.cp.base.total_units_of_type(unit_type)
        scheduled_units = self.pending_deliveries.units.get(unit_type, 0)

        unitName = QLabel(
            "<b>"
            + db.unit_get_expanded_info(
                self.game_model.game.player_country, unit_type, "name"
            )
            + "</b>"
        )
        unitName.setSizePolicy(
            QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        )

        existing_units = QLabel(str(existing_units))
        existing_units.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        amount_bought = QLabel("<b>{}</b>".format(str(scheduled_units)))
        amount_bought.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.existing_units_labels[unit_type] = existing_units
        self.bought_amount_labels[unit_type] = amount_bought

        price = QLabel("<b>$ {:02d}</b> m".format(db.PRICES[unit_type]))
        price.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        buysell = QGroupBox()
        buysell.setProperty("style", "buy-box")
        buysell.setMaximumHeight(36)
        buysell.setMinimumHeight(36)
        buysellayout = QHBoxLayout()
        buysell.setLayout(buysellayout)

        buy = QPushButton("+")
        buy.setProperty("style", "btn-buy")
        buy.setDisabled(not self.enable_purchase(unit_type))
        buy.setMinimumSize(16, 16)
        buy.setMaximumSize(16, 16)

        def on_buy():
            self.buy(unit_type)
            buy.setDisabled(not self.enable_purchase(unit_type))
            sell.setDisabled(not self.enable_sale(unit_type))

        buy.clicked.connect(on_buy)
        buy.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        sell = QPushButton("-")
        sell.setProperty("style", "btn-sell")
        sell.setDisabled(not self.enable_sale(unit_type))
        sell.setMinimumSize(16, 16)
        sell.setMaximumSize(16, 16)
        sell.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        def on_sell():
            self.sell(unit_type)
            sell.setDisabled(not self.enable_sale(unit_type))
            buy.setDisabled(not self.enable_purchase(unit_type))

        sell.clicked.connect(on_sell)

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

        buysellayout.addWidget(sell)
        buysellayout.addWidget(amount_bought)
        buysellayout.addWidget(buy)

        infolayout.addWidget(unitInfo)

        layout.addWidget(exist, row, 1)
        layout.addWidget(buysell, row, 2)
        layout.addWidget(info, row, 3)

        return row + 1

    def _update_count_label(self, unit_type: Type[UnitType]):

        self.bought_amount_labels[unit_type].setText(
            "<b>{}</b>".format(
                unit_type in self.pending_deliveries.units
                and "{}".format(self.pending_deliveries.units[unit_type])
                or "0"
            )
        )

        self.existing_units_labels[unit_type].setText(
            "<b>{}</b>".format(self.cp.base.total_units_of_type(unit_type))
        )

    def update_available_budget(self) -> None:
        GameUpdateSignal.get_instance().updateBudget(self.game_model.game)

    def buy(self, unit_type: Type[UnitType]):
        if not self.enable_purchase(unit_type):
            logging.error(f"Purchase of {unit_type.id} not allowed at {self.cp.name}")
            return

        price = db.PRICES[unit_type]
        self.pending_deliveries.order({unit_type: 1})
        self.budget -= price
        self._update_count_label(unit_type)
        self.update_available_budget()

    def sell(self, unit_type):
        if self.pending_deliveries.available_next_turn(unit_type) > 0:
            price = db.PRICES[unit_type]
            self.budget += price
            self.pending_deliveries.sell({unit_type: 1})
            if self.pending_deliveries.units[unit_type] == 0:
                del self.pending_deliveries.units[unit_type]
        self._update_count_label(unit_type)
        self.update_available_budget()

    def enable_purchase(self, unit_type: Type[UnitType]) -> bool:
        price = db.PRICES[unit_type]
        return self.budget >= price

    def enable_sale(self, unit_type: Type[UnitType]) -> bool:
        return True

    def info(self, unit_type):
        self.info_window = QUnitInfoWindow(self.game_model.game, unit_type)
        self.info_window.show()

    def set_maximum_units(self, maximum_units):
        """
        Set the maximum number of units that can be bought
        """
        self.maximum_units = maximum_units
