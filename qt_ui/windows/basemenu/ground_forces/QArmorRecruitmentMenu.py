from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QGroupBox

from game import Game
from game.event import UnitsDeliveryEvent
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour
from theater import ControlPoint, PinpointStrike, db


class QArmorRecruitmentMenu(QGroupBox, QRecruitBehaviour):

    def __init__(self, cp:ControlPoint, game:Game):
        QGroupBox.__init__(self, "Recruitment")
        self.cp = cp
        self.game = game

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        for event in self.game.events:
            if event.__class__ == UnitsDeliveryEvent and event.from_cp == self.cp:
                self.deliveryEvent = event
        if not self.deliveryEvent:
            self.deliveryEvent = self.game.units_delivery_event(self.cp)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        units = {
            PinpointStrike: db.find_unittype(PinpointStrike, self.game.player_name),
        }

        task_box_layout = QGridLayout()
        row = 0

        for task_type in units.keys():
            units_column = list(set(units[task_type]))
            if len(units_column) == 0: continue
            units_column.sort(key=lambda x: db.PRICES[x])
            for unit_type in units_column:
                row = self.add_purchase_row(unit_type, task_box_layout, row)
            stretch = QVBoxLayout()
            stretch.addStretch()
            task_box_layout.addLayout(stretch, row, 0)

        layout.addLayout(task_box_layout)
        layout.addStretch()
        self.setLayout(layout)
