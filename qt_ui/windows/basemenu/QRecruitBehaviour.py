from PySide2.QtWidgets import QLabel, QPushButton, \
    QSizePolicy, QSpacerItem
from dcs.unittype import UnitType

from theater import db


class QRecruitBehaviour:

    game = None
    cp = None
    deliveryEvent = None
    existing_units_labels = None
    bought_amount_labels = None

    def __init__(self):
        self.bought_amount_labels = {}
        self.existing_units_labels = {}

    def add_purchase_row(self, unit_type, layout, row):

        existing_units = self.cp.base.total_units_of_type(unit_type)
        scheduled_units = self.deliveryEvent.units.get(unit_type, 0)

        unitName = QLabel("<b>" + db.unit_type_name(unit_type) + "</b>")
        unitName.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        existing_units = QLabel(str(existing_units))
        existing_units.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        amount_bought = QLabel("[{}]".format(str(scheduled_units)))
        amount_bought.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.existing_units_labels[unit_type] = existing_units
        self.bought_amount_labels[unit_type] = amount_bought

        price = QLabel("{}m".format(db.PRICES[unit_type]))
        price.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        buy = QPushButton("+")
        buy.setProperty("style", "btn-success")
        buy.setMinimumSize(24, 24)
        buy.clicked.connect(lambda: self.buy(unit_type))
        buy.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        sell = QPushButton("-")
        sell.setProperty("style", "btn-danger")
        sell.setMinimumSize(24, 24)
        sell.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        sell.clicked.connect(lambda: self.sell(unit_type))

        layout.addWidget(unitName, row, 0)
        layout.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum), row, 1)
        layout.addWidget(existing_units, row, 2)
        layout.addWidget(amount_bought, row, 3)
        layout.addWidget(price, row, 4)
        layout.addItem(QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Minimum), row, 5)
        layout.addWidget(buy, row, 6)
        layout.addWidget(sell, row, 7)

        return row + 1

    def _update_count_label(self, unit_type: UnitType):

        self.bought_amount_labels[unit_type].setText("[{}]".format(
            unit_type in self.deliveryEvent.units and "{}".format(self.deliveryEvent.units[unit_type]) or "0"
        ))

        self.existing_units_labels[unit_type].setText("{}".format(
            self.cp.base.total_units_of_type(unit_type)
        ))

    def buy(self, unit_type):
        price = db.PRICES[unit_type]
        if self.game.budget >= price:
            self.deliveryEvent.deliver({unit_type: 1})
            self.game.budget -= price
        self._update_count_label(unit_type)

    def sell(self, unit_type):
        if self.deliveryEvent.units.get(unit_type, 0) > 0:
            price = db.PRICES[unit_type]
            self.game.budget += price
            self.deliveryEvent.units[unit_type] = self.deliveryEvent.units[unit_type] - 1
            if self.deliveryEvent.units[unit_type] == 0:
                del self.deliveryEvent.units[unit_type]
        elif self.cp.base.total_units_of_type(unit_type) > 0:
            price = db.PRICES[unit_type]
            self.game.budget += price
            self.cp.base.commit_losses({unit_type: 1})

        self._update_count_label(unit_type)
