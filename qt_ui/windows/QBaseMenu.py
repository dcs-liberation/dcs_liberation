from PySide2.QtCore import Qt
from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QFrame, QDialog, QVBoxLayout, QGridLayout, QPushButton
from dcs.unittype import UnitType

from theater import ControlPoint, CAP, Embarking, AirDefence, CAS, PinpointStrike, db
from game import Game


class QBaseMenu(QDialog):

    def __init__(self, parent, controlPoint: ControlPoint, game: Game):
        super(QBaseMenu, self).__init__(parent)
        self.cp = controlPoint
        self.game = game
        self.deliveryEvent = self.game.units_delivery_event(self.cp)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(200,200)
        self.initUi()

    def initUi(self):

        self.setWindowTitle(self.cp.name)

        self.topLayout = QHBoxLayout()
        self.topLayout.setProperty("style", "baseMenuHeader")
        self.topLayout.addWidget(QLabel("<b>" + self.cp.name + "</b>"))
        self.topLayout.addWidget(
            QLabel("{} / {} / {}".format(self.cp.base.total_planes, self.cp.base.total_armor, self.cp.base.total_aa)))

        units = {
            CAP: db.find_unittype(CAP, self.game.player_name),
            Embarking: db.find_unittype(Embarking, self.game.player_name),
            AirDefence: db.find_unittype(AirDefence, self.game.player_name),
            CAS: db.find_unittype(CAS, self.game.player_name),
            PinpointStrike: db.find_unittype(PinpointStrike, self.game.player_name),
        }

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topLayout)

        print(units)
        tasks = list(units.keys())
        tasks_per_column = 3

        self.bought_amount_labels = {}

        if self.cp.captured:
            column = 0
            for i, tasks_column in [(i, tasks[idx:idx+tasks_per_column]) for i, idx in enumerate(range(0, len(tasks), tasks_per_column))]:
                row = 2

                def purchase_row(unit_type, unit_price):
                    layout = QHBoxLayout()
                    existing_units = self.cp.base.total_units_of_type(unit_type)
                    scheduled_units = self.deliveryEvent.units.get(unit_type, 0)

                    unitName = QLabel(db.unit_type_name(unit_type))
                    amountBought = QLabel("{} ({})".format(existing_units, scheduled_units))
                    self.bought_amount_labels[unit_type] = amountBought

                    price = QLabel("{}m".format(unit_price))

                    buy = QPushButton("+")
                    buy.clicked.connect(lambda: self.buy(unit_type))

                    sell = QPushButton("-")
                    sell.clicked.connect(lambda: self.sell(unit_type))

                    layout.addWidget(unitName)
                    layout.addWidget(amountBought)
                    layout.addWidget(price)

                    layout.addWidget(buy)
                    layout.addWidget(sell)

                    return layout

                for task_type in tasks_column:
                    QLabel("<b>{}</b>".format(db.task_name(task_type)))
                    row += 1

                    units_column = list(set(units[task_type]))
                    units_column.sort(key=lambda x: db.PRICES[x])
                    for unit_type in units_column:
                        layout = purchase_row(unit_type, db.PRICES[unit_type])
                        self.mainLayout.addLayout(layout)

                column += 5


        self.setLayout(self.mainLayout)


    def _update_count_label(self, unit_type: UnitType):
        self.bought_amount_labels[unit_type].setText("({}{})".format(
            self.cp.base.total_units_of_type(unit_type),
            unit_type in self.deliveryEvent.units and ", bought {}".format(self.deliveryEvent.units[unit_type]) or ""
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