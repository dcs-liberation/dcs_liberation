from PySide2.QtWidgets import QLabel, QPushButton, \
    QSizePolicy, QSpacerItem, QGroupBox, QHBoxLayout
from dcs.unittype import UnitType

from theater import db

class QRecruitBehaviour:

    game = None
    cp = None
    deliveryEvent = None
    existing_units_labels = None
    bought_amount_labels = None
    BUDGET_FORMAT = "Available Budget: <b>${}M</b>"

    def __init__(self):
        self.bought_amount_labels = {}
        self.existing_units_labels = {}
        self.update_available_budget()

    def add_purchase_row(self, unit_type, layout, row):

        exist = QGroupBox()
        exist.setProperty("style", "buy-box")
        exist.setMaximumHeight(36)
        exist.setMinimumHeight(36)
        existLayout = QHBoxLayout()
        exist.setLayout(existLayout)

        existing_units = self.cp.base.total_units_of_type(unit_type)
        scheduled_units = self.deliveryEvent.units.get(unit_type, 0)

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
        buy.setMinimumSize(16, 16)
        buy.setMaximumSize(16, 16)
        buy.clicked.connect(lambda: self.buy(unit_type))
        buy.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        sell = QPushButton("-")
        sell.setProperty("style", "btn-sell")
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

    def _update_count_label(self, unit_type: UnitType):

        self.bought_amount_labels[unit_type].setText("<b>{}</b>".format(
            unit_type in self.deliveryEvent.units and "{}".format(self.deliveryEvent.units[unit_type]) or "0"
        ))

        self.existing_units_labels[unit_type].setText("<b>{}</b>".format(
            self.cp.base.total_units_of_type(unit_type)
        ))

    def update_available_budget(self):
        parent = self.parent()
        while parent.objectName != "menuDialogue":
            parent = parent.parent()
        for child in parent.children():
            if child.objectName() == "budgetField":
                child.setText(QRecruitBehaviour.BUDGET_FORMAT.format(self.game.budget))

    def buy(self, unit_type):

        price = db.PRICES[unit_type]
        if self.game.budget >= price:
            self.deliveryEvent.deliver({unit_type: 1})
            self.game.budget -= price
        self._update_count_label(unit_type)
        self.update_available_budget()

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
        self.update_available_budget()
