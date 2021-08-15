from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QScrollArea, QVBoxLayout, QWidget

from game.dcs.groundunittype import GroundUnitType
from game.theater import ControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.UnitTransactionFrame import UnitTransactionFrame
from game.purchaseadapter import GroundUnitPurchaseAdapter


class QArmorRecruitmentMenu(UnitTransactionFrame[GroundUnitType]):
    def __init__(self, cp: ControlPoint, game_model: GameModel):
        super().__init__(
            game_model,
            GroundUnitPurchaseAdapter(
                cp, game_model.game.coalition_for(cp.captured), game_model.game
            ),
        )
        self.cp = cp
        self.game_model = game_model
        self.purchase_groups = {}
        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        scroll_content.setLayout(task_box_layout)
        row = 0

        unit_types = list(
            set(self.game_model.game.faction_for(player=True).ground_units)
        )
        unit_types.sort(key=lambda u: u.name)
        for row, unit_type in enumerate(unit_types):
            self.add_purchase_row(unit_type, task_box_layout, row)
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
