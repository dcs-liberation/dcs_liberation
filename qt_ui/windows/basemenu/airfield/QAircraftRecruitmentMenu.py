from typing import Set

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from game.dcs.aircrafttype import AircraftType
from game.squadrons import Squadron
from game.theater import ControlPoint
from qt_ui.models import GameModel
from qt_ui.uiconstants import ICONS
from qt_ui.windows.basemenu.UnitTransactionFrame import UnitTransactionFrame
from game.purchaseadapter import AircraftPurchaseAdapter


class QAircraftRecruitmentMenu(UnitTransactionFrame[Squadron]):
    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        super().__init__(game_model, AircraftPurchaseAdapter(cp))
        self.cp = cp
        self.game_model = game_model
        self.purchase_groups = {}
        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.hangar_status = QHangarStatus(game_model, self.cp)

        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        row = 0

        unit_types: Set[AircraftType] = set()

        for squadron in cp.squadrons:
            unit_types.add(squadron.aircraft)

        sorted_squadrons = sorted(cp.squadrons, key=lambda s: (s.aircraft.name, s.name))
        for row, squadron in enumerate(sorted_squadrons):
            self.add_purchase_row(squadron, task_box_layout, row)

        stretch = QVBoxLayout()
        stretch.addStretch()
        task_box_layout.addLayout(stretch, row, 0)

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addLayout(self.hangar_status)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def sell_tooltip(self, is_enabled: bool) -> str:
        if is_enabled:
            return "Sell unit. Use Shift or Ctrl key to sell multiple units at once."
        else:
            return (
                "Can not be sold because either no aircraft are available or are "
                "already assigned to a mission."
            )

    def post_transaction_update(self) -> None:
        super().post_transaction_update()
        self.hangar_status.update_label()


class QHangarStatus(QHBoxLayout):
    def __init__(self, game_model: GameModel, control_point: ControlPoint) -> None:
        super().__init__()
        self.game_model = game_model
        self.control_point = control_point

        self.icon = QLabel()
        self.icon.setPixmap(ICONS["Hangar"])
        self.text = QLabel("")

        self.update_label()
        self.addWidget(self.icon, Qt.AlignLeft)
        self.addWidget(self.text, Qt.AlignLeft)
        self.addStretch(50)
        self.setAlignment(Qt.AlignLeft)

    def update_label(self) -> None:
        next_turn = self.control_point.allocated_aircraft()
        max_amount = self.control_point.total_aircraft_parking

        components = [f"{next_turn.total_present} present"]
        if next_turn.total_ordered > 0:
            components.append(f"{next_turn.total_ordered} purchased")
        elif next_turn.total_ordered < 0:
            components.append(f"{-next_turn.total_ordered} sold")

        transferring = next_turn.total_transferring
        if transferring > 0:
            components.append(f"{transferring} transferring in")
        if transferring < 0:
            components.append(f"{-transferring} transferring out")

        details = ", ".join(components)
        self.text.setText(
            f"<strong>{next_turn.total}/{max_amount}</strong> ({details})"
        )
