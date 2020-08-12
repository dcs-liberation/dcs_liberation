from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QGroupBox, QFrame, QWidget, QScrollArea

from game import Game
from game.event import UnitsDeliveryEvent
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour
from theater import ControlPoint, PinpointStrike, db


class QArmorRecruitmentMenu(QFrame, QRecruitBehaviour):

    def __init__(self, cp:ControlPoint, game:Game):
        QFrame.__init__(self)
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
        main_layout = QVBoxLayout()

        units = {
            PinpointStrike: db.find_unittype(PinpointStrike, self.game.player_name),
        }

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        scroll_content.setLayout(task_box_layout)
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

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)