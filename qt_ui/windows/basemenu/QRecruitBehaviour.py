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
from game.event import UnitsDeliveryEvent
from game.theater import ControlPoint
from qt_ui.models import GameModel


class QRecruitBehaviour:
    game_model: GameModel
    cp: ControlPoint
    existing_units_labels = None
    bought_amount_labels = None
    maximum_units = -1
    recruitable_types = []
    BUDGET_FORMAT = "Available Budget: <b>${}M</b>"

    def __init__(self) -> None:
        self.bought_amount_labels = {}
        self.existing_units_labels = {}
        self.recruitable_types = []
        self.update_available_budget()

    @property
    def pending_deliveries(self) -> UnitsDeliveryEvent:
        assert self.cp.pending_unit_deliveries
        return self.cp.pending_unit_deliveries

    @property
    def budget(self) -> int:
        return self.game_model.game.budget

    @budget.setter
    def budget(self, value: int) -> None:
        self.game_model.game.budget = value

    def add_purchase_row(self, unit_type: Type[UnitType], layout: QLayout,
                         row: int, disabled: bool = False) -> int:
        exist = QGroupBox()
        exist.setProperty("style", "buy-box")
        exist.setMaximumHeight(36)
        exist.setMinimumHeight(36)
        existLayout = QHBoxLayout()
        exist.setLayout(existLayout)

        existing_units = self.cp.base.total_units_of_type(unit_type)
        scheduled_units = self.pending_deliveries.units.get(unit_type, 0)

        unitName = QLabel("<b>" + db.unit_type_name_2(unit_type) + "</b>")
        unitName.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

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
        buy.setDisabled(disabled)
        buy.setMinimumSize(16, 16)
        buy.setMaximumSize(16, 16)
        buy.clicked.connect(lambda: self.buy(unit_type))
        buy.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        sell = QPushButton("-")
        sell.setProperty("style", "btn-sell")
        sell.setDisabled(disabled)
        sell.setMinimumSize(16, 16)
        sell.setMaximumSize(16, 16)
        sell.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sell.clicked.connect(lambda: self.sell(unit_type))

        existLayout.addWidget(unitName)
        existLayout.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        existLayout.addWidget(existing_units)
        existLayout.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum))
        existLayout.addWidget(price)

        buysellayout.addWidget(sell)
        buysellayout.addWidget(amount_bought)
        buysellayout.addWidget(buy)

        layout.addWidget(exist, row, 1)
        layout.addWidget(buysell, row, 2)

        return row + 1

    def _update_count_label(self, unit_type: Type[UnitType]):

        self.bought_amount_labels[unit_type].setText("<b>{}</b>".format(
            unit_type in self.pending_deliveries.units and "{}".format(self.pending_deliveries.units[unit_type]) or "0"
        ))

        self.existing_units_labels[unit_type].setText("<b>{}</b>".format(
            self.cp.base.total_units_of_type(unit_type)
        ))

    def update_available_budget(self):
        parent = self.parent()
        while parent.objectName != "menuDialogue":
            parent = parent.parent()
        parent.update_dialogue_budget(self.budget)

    def buy(self, unit_type: Type[UnitType]):
        price = db.PRICES[unit_type]
        if self.budget >= price:
            self.pending_deliveries.deliver({unit_type: 1})
            self.budget -= price
        else:
            # TODO : display modal warning
            logging.info("Not enough money !")
        self._update_count_label(unit_type)
        self.update_available_budget()

    def sell(self, unit_type):
        if self.pending_deliveries.units.get(unit_type, 0) > 0:
            price = db.PRICES[unit_type]
            self.budget += price
            self.pending_deliveries.units[unit_type] = self.pending_deliveries.units[unit_type] - 1
            if self.pending_deliveries.units[unit_type] == 0:
                del self.pending_deliveries.units[unit_type]
        elif self.cp.base.total_units_of_type(unit_type) > 0:
            price = db.PRICES[unit_type]
            self.budget += price
            self.cp.base.commit_losses({unit_type: 1})

        self._update_count_label(unit_type)
        self.update_available_budget()

    def set_maximum_units(self, maximum_units):
        """
        Set the maximum number of units that can be bought
        """
        self.maximum_units = maximum_units

    def set_recruitable_types(self, recruitables_types):
        """
        Set the maximum number of units that can be bought
        """
        self.recruitables_types = recruitables_types
