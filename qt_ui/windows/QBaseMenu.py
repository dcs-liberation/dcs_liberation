import traceback

from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QDialog, QVBoxLayout, QGridLayout, QPushButton, \
    QGroupBox, QSizePolicy, QSpacerItem
from dcs.unittype import UnitType

from game.event import UnitsDeliveryEvent
from qt_ui.widgets.base.QAirportInformation import QAirportInformation
from qt_ui.widgets.base.QBaseInformation import QBaseInformation
from qt_ui.widgets.base.QPlannedFlightView import QPlannedFlightView
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from theater import ControlPoint, CAP, Embarking, CAS, PinpointStrike, db
from game import Game


class QBaseMenu(QDialog):

    def __init__(self, parent, controlPoint: ControlPoint, game: Game):
        super(QBaseMenu, self).__init__(parent)

        self.cp = controlPoint
        self.game = game

        try:
            self.airport = game.theater.terrain.airport_by_id(self.cp.id)
        except:
            self.airport = None

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
        title.setProperty("style", "base-title")
        unitsPower = QLabel("{} / {}".format(self.cp.base.total_planes, self.cp.base.total_armor))

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
            }
        else:
            units = {
                CAP: db.find_unittype(CAP, self.game.enemy_name),
                Embarking: db.find_unittype(Embarking, self.game.enemy_name),
                CAS: db.find_unittype(CAS, self.game.enemy_name),
                PinpointStrike: db.find_unittype(PinpointStrike, self.game.enemy_name),
            }

        self.mainLayout = QGridLayout()
        self.leftLayout = QVBoxLayout()
        self.unitLayout = QVBoxLayout()
        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        row = 0

        if self.cp.captured:

            self.recruitment = QGroupBox("Recruitment")
            self.recruitmentLayout = QVBoxLayout()

            for task_type in units.keys():

                units_column = list(set(units[task_type]))
                if len(units_column) == 0: continue
                units_column.sort(key=lambda x: db.PRICES[x])

                task_box = QGroupBox("{}".format(db.task_name(task_type)))
                task_box_layout = QGridLayout()
                task_box.setLayout(task_box_layout)
                row = 0
                for unit_type in units_column:
                    row = self.add_purchase_row(unit_type, task_box_layout, row)

                stretch = QVBoxLayout()
                stretch.addStretch()
                task_box_layout.addLayout(stretch, row, 0)

                self.recruitmentLayout.addWidget(task_box)
                self.recruitmentLayout.addStretch()

            self.recruitment.setLayout(self.recruitmentLayout)
            self.leftLayout.addWidget(self.recruitment)
            self.leftLayout.addStretch()
        else:
            intel = QGroupBox("Intel")
            intelLayout = QVBoxLayout()

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
            intelLayout.addStretch()
            intel.setLayout(intelLayout)
            self.leftLayout.addWidget(intel)

        self.mainLayout.addWidget(self.topLayoutWidget, 0, 0)
        self.mainLayout.addLayout(self.leftLayout, 1, 0)
        self.mainLayout.addWidget(QBaseInformation(self.cp, self.airport), 1, 1)

        self.rightLayout = QVBoxLayout()
        try:
            self.rightLayout.addWidget(QPlannedFlightView(self.game.planners[self.cp.id]))
        except Exception:
            traceback.print_exc()
        self.rightLayout.addWidget(QAirportInformation(self.cp, self.airport))
        self.mainLayout.addLayout(self.rightLayout, 1, 2)

        self.setLayout(self.mainLayout)

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

    def closeEvent(self, closeEvent:QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game)