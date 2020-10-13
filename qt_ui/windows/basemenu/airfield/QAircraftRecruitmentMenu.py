from typing import Optional, Set

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from dcs.unittype import UnitType

from game.event.event import UnitsDeliveryEvent
from qt_ui.models import GameModel
from qt_ui.uiconstants import ICONS
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour
from theater import CAP, CAS, ControlPoint, db


class QAircraftRecruitmentMenu(QFrame, QRecruitBehaviour):
    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        QFrame.__init__(self)
        self.cp = cp
        self.game_model = game_model
        self.deliveryEvent: Optional[UnitsDeliveryEvent] = None

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        for event in self.game_model.game.events:
            if event.__class__ == UnitsDeliveryEvent and event.from_cp == self.cp:
                self.deliveryEvent = event
        if not self.deliveryEvent:
            self.deliveryEvent = self.game_model.game.units_delivery_event(self.cp)

        # Determine maximum number of aircrafts that can be bought
        self.set_maximum_units(self.cp.available_aircraft_slots)
        self.set_recruitable_types([CAP, CAS])

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.hangar_status = QHangarStatus(self.total_units, self.cp.available_aircraft_slots)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        tasks = [CAP, CAS]

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        row = 0

        unit_types: Set[UnitType] = set()
        for task in tasks:
            units = db.find_unittype(task, self.game_model.game.player_name)
            if not units:
                continue
            for unit in units:
                if self.cp.is_carrier and unit not in db.CARRIER_CAPABLE:
                    continue
                if self.cp.is_lha and unit not in db.LHA_CAPABLE:
                    continue
                unit_types.add(unit)

        sorted_units = sorted(unit_types, key=lambda u: db.unit_type_name_2(u))
        for unit_type in sorted_units:
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
        main_layout.addLayout(self.hangar_status)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def buy(self, unit_type):
        super().buy(unit_type)
        self.hangar_status.update_label(self.total_units, self.cp.available_aircraft_slots)

    def sell(self, unit_type):
        super().sell(unit_type)
        self.hangar_status.update_label(self.total_units, self.cp.available_aircraft_slots)


class QHangarStatus(QHBoxLayout):

    def __init__(self, current_amount: int, max_amount: int):
        super(QHangarStatus, self).__init__()
        self.icon = QLabel()
        self.icon.setPixmap(ICONS["Hangar"])
        self.text = QLabel("")

        self.update_label(current_amount, max_amount)
        self.addWidget(self.icon, Qt.AlignLeft)
        self.addWidget(self.text, Qt.AlignLeft)
        self.addStretch(50)
        self.setAlignment(Qt.AlignLeft)

    def update_label(self, current_amount: int, max_amount: int):
        self.text.setText("<strong>{}/{}</strong>".format(current_amount, max_amount))
