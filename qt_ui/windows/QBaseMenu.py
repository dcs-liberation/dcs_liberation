from PySide2.QtCore import Qt
from PySide2.QtGui import QWindow, QCloseEvent
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QFrame, QDialog, QVBoxLayout, QGridLayout, QPushButton, \
    QGroupBox
from dcs.unittype import UnitType

from game.event import UnitsDeliveryEvent
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from theater import ControlPoint, CAP, Embarking, AirDefence, CAS, PinpointStrike, db
from game import Game


class QBaseMenu(QDialog):

    def __init__(self, parent, controlPoint: ControlPoint, game: Game):
        super(QBaseMenu, self).__init__(parent)
        self.cp = controlPoint
        self.game = game


        if self.cp.captured:
            self.deliveryEvent = None
            for event in self.game.events:
                print(event.__class__)
                print(UnitsDeliveryEvent.__class__)
                if event.__class__ == UnitsDeliveryEvent and event.from_cp == self.cp:
                    self.deliveryEvent = event
                    break
            if not self.deliveryEvent:
                print("Rebuild event")
                self.deliveryEvent = self.game.units_delivery_event(self.cp)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(300, 200)
        self.setModal(True)
        self.initUi()

    def initUi(self):

        self.setWindowTitle(self.cp.name)

        self.topLayoutWidget = QWidget()
        self.topLayout = QHBoxLayout()

        title = QLabel("<b>" + self.cp.name + "</b>")
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        unitsPower = QLabel("{} / {} / {}".format(self.cp.base.total_planes, self.cp.base.total_armor, self.cp.base.total_aa))
        unitsPower.setAlignment(Qt.AlignLeft |Qt.AlignTop)

        self.topLayout.addWidget(title)
        self.topLayout.addWidget(unitsPower)
        self.topLayout.setAlignment(Qt.AlignTop)
        self.topLayoutWidget.setProperty("style", "baseMenuHeader")
        self.topLayoutWidget.setLayout(self.topLayout)

        if self.cp.captured:
            units = {
                CAP: db.find_unittype(CAP, self.game.player_name),
                Embarking: db.find_unittype(Embarking, self.game.player_name),
                CAS: db.find_unittype(CAS, self.game.player_name),
                PinpointStrike: db.find_unittype(PinpointStrike, self.game.player_name),
                AirDefence: db.find_unittype(AirDefence, self.game.player_name),
            }
        else:
            units = {
                CAP: db.find_unittype(CAP, self.game.enemy_name),
                Embarking: db.find_unittype(Embarking, self.game.enemy_name),
                AirDefence: db.find_unittype(AirDefence, self.game.enemy_name),
                CAS: db.find_unittype(CAS, self.game.enemy_name),
                PinpointStrike: db.find_unittype(PinpointStrike, self.game.enemy_name),
            }

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.topLayoutWidget)

        tasks = list(units.keys())
        tasks_per_column = 3

        self.unitLayout = QGridLayout()
        self.bought_amount_labels = {}

        row = 0

        def add_purchase_row(unit_type):

            nonlocal row
            existing_units = self.cp.base.total_units_of_type(unit_type)
            scheduled_units = self.deliveryEvent.units.get(unit_type, 0)

            unitName = QLabel("<b>" + db.unit_type_name(unit_type) + "</b>")
            amountBought = QLabel("{} ({})".format(existing_units, scheduled_units))
            self.bought_amount_labels[unit_type] = amountBought

            price = QLabel("{}m".format(db.PRICES[unit_type]))

            buy = QPushButton("+")
            buy.clicked.connect(lambda: self.buy(unit_type))

            sell = QPushButton("-")
            sell.clicked.connect(lambda: self.sell(unit_type))

            self.unitLayout.addWidget(unitName, row, 0)
            self.unitLayout.addWidget(amountBought, row, 1)
            self.unitLayout.addWidget(price, row, 2)
            self.unitLayout.addWidget(buy, row, 3)
            self.unitLayout.addWidget(sell, row, 4)

            row = row + 1

        if self.cp.captured:

            for task_type in units.keys():

                units_column = list(set(units[task_type]))
                if len(units_column) == 0: continue
                units_column.sort(key=lambda x: db.PRICES[x])

                taskTypeLabel = QLabel("<b>{}</b>".format(db.task_name(task_type)))
                self.unitLayout.addWidget(taskTypeLabel, row, 0)
                row = row + 1

                for unit_type in units_column:
                    add_purchase_row(unit_type)
            self.mainLayout.addLayout(self.unitLayout)
        else:
            intel = QGroupBox("Intel")
            intelLayout = QVBoxLayout()

            row = 0
            for task_type in units.keys():
                units_column = list(set(units[task_type]))

                if sum([self.cp.base.total_units_of_type(u) for u in units_column]) > 0:

                    group = QGroupBox(db.task_name(task_type))
                    groupLayout = QGridLayout()
                    group.setLayout(groupLayout)

                    row = 0
                    for unit_type in units_column:
                        existing_units = self.cp.base.total_units_of_type(unit_type)
                        if existing_units == 0:
                            continue
                        groupLayout.addWidget(QLabel("<b>" + db.unit_type_name(unit_type) + "</b>"), row, 0)
                        groupLayout.addWidget(QLabel(str(existing_units)), row, 1)
                        row += 1

                    intelLayout.addWidget(group)
            self.mainLayout.addLayout(intelLayout)

        self.setLayout(self.mainLayout)


    def _update_count_label(self, unit_type: UnitType):
        self.bought_amount_labels[unit_type].setText("{}{}".format(
            self.cp.base.total_units_of_type(unit_type),
            unit_type in self.deliveryEvent.units and " ({})".format(self.deliveryEvent.units[unit_type]) or ""
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

    def closeEvent(self, closeEvent:QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game)