import logging
from typing import Optional, Set, Type

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from dcs.helicopters import helicopter_map
from dcs.task import CAP, CAS, AWACS, Refueling, Transport
from dcs.unittype import FlyingType, UnitType

from game import db
from game.theater import ControlPoint, ControlPointType
from qt_ui.models import GameModel
from qt_ui.uiconstants import ICONS
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour


class QAircraftRecruitmentMenu(QFrame, QRecruitBehaviour):
    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        QFrame.__init__(self)
        self.cp = cp
        self.game_model = game_model

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        # Determine maximum number of aircrafts that can be bought
        self.set_maximum_units(self.cp.total_aircraft_parking)

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.hangar_status = QHangarStatus(game_model, self.cp)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        tasks = [CAP, CAS, AWACS, Refueling, Transport]

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        row = 0

        unit_types: Set[Type[FlyingType]] = set()
        for unit_type in self.game_model.game.player_faction.aircrafts:
            if not issubclass(unit_type, FlyingType):
                raise RuntimeError(f"Non-flying aircraft found in faction: {unit_type}")
            if self.cp.is_carrier and unit_type not in db.CARRIER_CAPABLE:
                continue
            if self.cp.is_lha and unit_type not in db.LHA_CAPABLE:
                continue
            if (
                self.cp.cptype in [ControlPointType.FOB, ControlPointType.FARP]
                and unit_type not in helicopter_map.values()
            ):
                continue
            unit_types.add(unit_type)

        sorted_units = sorted(
            unit_types,
            key=lambda u: db.unit_get_expanded_info(
                self.game_model.game.player_country, u, "name"
            ),
        )
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

    def enable_purchase(self, unit_type: Type[UnitType]) -> bool:
        if not super().enable_purchase(unit_type):
            return False
        if not issubclass(unit_type, FlyingType):
            return False
        if not self.cp.can_operate(unit_type):
            return False
        return True

    def enable_sale(self, unit_type: Type[UnitType]) -> bool:
        if not issubclass(unit_type, FlyingType):
            return False
        if not self.cp.can_operate(unit_type):
            return False
        return True

    def buy(self, unit_type):
        if self.maximum_units > 0:
            if self.cp.unclaimed_parking(self.game_model.game) <= 0:
                logging.debug(f"No space for additional aircraft at {self.cp}.")
                QMessageBox.warning(
                    self,
                    "No space for additional aircraft",
                    f"There is no parking space left at {self.cp.name} to accommodate another plane.",
                    QMessageBox.Ok,
                )
                return
            # If we change our mind about selling, we want the aircraft to be put
            # back in the inventory immediately.
            elif self.pending_deliveries.units.get(unit_type, 0) < 0:
                global_inventory = self.game_model.game.aircraft_inventory
                inventory = global_inventory.for_control_point(self.cp)
                inventory.add_aircraft(unit_type, 1)

        super().buy(unit_type)
        self.hangar_status.update_label()

    def sell(self, unit_type: UnitType):
        # Don't need to remove aircraft from the inventory if we're canceling
        # orders.
        if self.pending_deliveries.units.get(unit_type, 0) <= 0:
            global_inventory = self.game_model.game.aircraft_inventory
            inventory = global_inventory.for_control_point(self.cp)
            try:
                inventory.remove_aircraft(unit_type, 1)
            except ValueError:
                QMessageBox.critical(
                    self,
                    "Could not sell aircraft",
                    f"Attempted to sell one {unit_type.id} at {self.cp.name} "
                    "but none are available. Are all aircraft currently "
                    "assigned to a mission?",
                    QMessageBox.Ok,
                )
                return
        super().sell(unit_type)
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
        next_turn = self.control_point.expected_aircraft_next_turn(self.game_model.game)
        max_amount = self.control_point.total_aircraft_parking

        components = [f"{next_turn.present} present"]
        if next_turn.ordered > 0:
            components.append(f"{next_turn.ordered} purchased")
        elif next_turn.ordered < 0:
            components.append(f"{-next_turn.ordered} sold")

        transferring = next_turn.transferring
        if transferring > 0:
            components.append(f"{transferring} transferring in")
        if transferring < 0:
            components.append(f"{-transferring} transferring out")

        details = ", ".join(components)
        self.text.setText(
            f"<strong>{next_turn.total}/{max_amount}</strong> ({details})"
        )
