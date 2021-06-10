from typing import Type

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from dcs.unittype import UnitType

from game import db
from game.theater import ControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour


class QArmorRecruitmentMenu(QFrame, QRecruitBehaviour):
    def __init__(self, cp: ControlPoint, game_model: GameModel):
        QFrame.__init__(self)
        self.cp = cp
        self.game_model = game_model

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        scroll_content.setLayout(task_box_layout)
        row = 0

        unit_types = list(
            set(self.game_model.game.faction_for(player=True).ground_units)
        )
        unit_types.sort(
            key=lambda u: db.unit_get_expanded_info(
                self.game_model.game.player_country, u, "name"
            )
        )
        for unit_type in unit_types:
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

    def enable_purchase(self, unit_type: Type[UnitType]) -> bool:
        if not super().enable_purchase(unit_type):
            return False
        return self.cp.has_ground_unit_source(self.game_model.game)

    def enable_sale(self, unit_type: Type[UnitType]) -> bool:
        return self.pending_deliveries.pending_orders(unit_type) > 0
