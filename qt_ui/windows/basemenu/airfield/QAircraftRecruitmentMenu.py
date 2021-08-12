import logging
from typing import Set

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

from game.dcs.aircrafttype import AircraftType
from game.theater import ControlPoint, ControlPointType
from qt_ui.models import GameModel
from qt_ui.uiconstants import ICONS
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour


class QAircraftRecruitmentMenu(QFrame, QRecruitBehaviour):
    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        QFrame.__init__(self)
        self.cp = cp
        self.game_model = game_model
        self.purchase_groups = {}
        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        # Determine maximum number of aircrafts that can be bought
        self.set_maximum_units(self.cp.total_aircraft_parking)

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.hangar_status = QHangarStatus(game_model, self.cp)

        main_layout = QVBoxLayout()

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        row = 0

        unit_types: Set[AircraftType] = set()
        for unit_type in self.game_model.game.blue.faction.aircrafts:
            if self.cp.is_carrier and not unit_type.carrier_capable:
                continue
            if self.cp.is_lha and not unit_type.lha_capable:
                continue
            if (
                self.cp.cptype in [ControlPointType.FOB, ControlPointType.FARP]
                and unit_type not in helicopter_map.values()
            ):
                continue
            unit_types.add(unit_type)

        sorted_units = sorted(
            unit_types,
            key=lambda u: u.name,
        )
        for row, unit_type in enumerate(sorted_units):
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
        main_layout.addLayout(self.hangar_status)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def enable_purchase(self, unit_type: AircraftType) -> bool:
        if not super().enable_purchase(unit_type):
            return False
        if not self.cp.can_operate(unit_type):
            return False
        return True

    def enable_sale(self, unit_type: AircraftType) -> bool:
        return self.can_be_sold(unit_type)

    def sell_tooltip(self, is_enabled: bool) -> str:
        if is_enabled:
            return "Sell unit. Use Shift or Ctrl key to sell multiple units at once."
        else:
            return "Can not be sold because either no aircraft are available or are already assigned to a mission."

    def buy(self, unit_type: AircraftType) -> bool:
        if self.maximum_units > 0:
            if self.cp.unclaimed_parking(self.game_model.game) <= 0:
                logging.debug(f"No space for additional aircraft at {self.cp}.")
                QMessageBox.warning(
                    self,
                    "No space for additional aircraft",
                    f"There is no parking space left at {self.cp.name} to accommodate "
                    "another plane.",
                    QMessageBox.Ok,
                )
                return False
            # If we change our mind about selling, we want the aircraft to be put
            # back in the inventory immediately.
            elif self.pending_deliveries.units.get(unit_type, 0) < 0:
                global_inventory = self.game_model.game.aircraft_inventory
                inventory = global_inventory.for_control_point(self.cp)
                inventory.add_aircraft(unit_type, 1)

        super().buy(unit_type)
        self.hangar_status.update_label()
        return True

    def can_be_sold(self, unit_type: AircraftType) -> bool:
        inventory = self.game_model.game.aircraft_inventory.for_control_point(self.cp)
        pending_deliveries = self.pending_deliveries.units.get(unit_type, 0)
        return self.cp.can_operate(unit_type) and (
            pending_deliveries > 0 or inventory.available(unit_type) > 0
        )

    def sell(self, unit_type: AircraftType) -> bool:
        # Don't need to remove aircraft from the inventory if we're canceling
        # orders.
        if not self.can_be_sold(unit_type):
            QMessageBox.critical(
                self,
                "Could not sell aircraft",
                f"Attempted to sell one {unit_type} at {self.cp.name} "
                "but none are available. Are all aircraft currently "
                "assigned to a mission?",
                QMessageBox.Ok,
            )
            return False

        inventory = self.game_model.game.aircraft_inventory.for_control_point(self.cp)
        pending_deliveries = self.pending_deliveries.units.get(unit_type, 0)
        if pending_deliveries <= 0 < inventory.available(unit_type):
            inventory.remove_aircraft(unit_type, 1)

        super().sell(unit_type)
        self.hangar_status.update_label()

        return True


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
        next_turn = self.control_point.allocated_aircraft(self.game_model.game)
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
