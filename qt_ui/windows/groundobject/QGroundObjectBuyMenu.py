import logging
from typing import Optional

from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QCheckBox,
)

from game import Game
from game.data.groups import GroupRole, ROLE_TASKINGS, GroupTask
from game.point_with_heading import PointWithHeading
from game.theater import TheaterGroundObject
from game.theater.theatergroundobject import (
    VehicleGroupGroundObject,
    SamGroundObject,
    EwrGroundObject,
    GroundGroup,
)
from gen.templates import (
    GroundObjectTemplate,
    GroupTemplate,
)
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal


class QGroundObjectGroupTemplate(QGroupBox):
    group_template_changed = Signal(GroupTemplate)
    # UI to show one GroupTemplate and configure the TemplateRandomizer for it
    # one row: [Required | Unit Selector | Amount | Price]
    # If the group is not randomizable: Just view labels instead of edit fields

    def __init__(self, group_id: int, group_template: GroupTemplate) -> None:
        super(QGroundObjectGroupTemplate, self).__init__(
            f"{group_id + 1}: {group_template.name}"
        )
        self.group_template = group_template

        self.group_layout = QGridLayout()
        self.setLayout(self.group_layout)

        self.amount_selector = QSpinBox()
        self.unit_selector = QComboBox()
        self.group_selector = QCheckBox()

        self.group_selector.setChecked(self.group_template.should_be_generated)
        self.group_selector.setEnabled(self.group_template.optional)

        if self.group_template.can_be_modified:
            # Group can be modified (more than 1 possible unit_type for the group)
            for unit in self.group_template.possible_units:
                self.unit_selector.addItem(f"{unit} [${unit.price}M]", userData=unit)
            self.group_layout.addWidget(
                self.unit_selector, 0, 0, alignment=Qt.AlignRight
            )
            self.group_layout.addWidget(
                self.amount_selector, 0, 1, alignment=Qt.AlignRight
            )

            self.amount_selector.setMinimum(1)
            self.amount_selector.setMaximum(self.group_template.max_size)
            self.amount_selector.setValue(self.group_template.size)

            self.on_group_changed()
        else:
            # Group can not be randomized so just show the group info
            group_info = QVBoxLayout()
            try:
                unit_name = next(self.group_template.possible_units)
            except StopIteration:
                unit_name = self.group_template.unit_type
            group_info.addWidget(
                QLabel(f"{self.group_template.size}x {unit_name}"),
                alignment=Qt.AlignLeft,
            )
            self.group_layout.addLayout(group_info, 0, 0, 1, 2)

        self.group_layout.addWidget(self.group_selector, 0, 2, alignment=Qt.AlignRight)

        self.amount_selector.valueChanged.connect(self.on_group_changed)
        self.unit_selector.currentIndexChanged.connect(self.on_group_changed)
        self.group_selector.stateChanged.connect(self.on_group_changed)

    def on_group_changed(self) -> None:
        self.group_template.set_enabled(self.group_selector.isChecked())
        if self.group_template.can_be_modified:
            unit_type = self.unit_selector.itemData(self.unit_selector.currentIndex())
            self.group_template.unit_count = [self.amount_selector.value()]
            self.group_template.set_unit_type(unit_type.dcs_id)
        self.group_template_changed.emit(self.group_template)


class QGroundObjectTemplateLayout(QGroupBox):
    def __init__(
        self,
        game: Game,
        ground_object: TheaterGroundObject,
        template_changed_signal: Signal(GroundObjectTemplate),
        current_group_value: int,
    ):
        super(QGroundObjectTemplateLayout, self).__init__("Groups:")
        # Connect to the signal to handle template updates
        self.game = game
        self.ground_object = ground_object
        self.template_changed_signal = template_changed_signal
        self.template_changed_signal.connect(self.load_for_template)
        self.template: Optional[GroundObjectTemplate] = None

        self.current_group_value = current_group_value

        self.buy_button = QPushButton("Buy")
        self.buy_button.clicked.connect(self.buy_group)

        self.template_layout = QGridLayout()
        self.setLayout(self.template_layout)

        self.template_grid = QGridLayout()
        self.template_layout.addLayout(self.template_grid, 0, 0, 1, 2)
        self.template_layout.addWidget(self.buy_button, 1, 1)
        stretch = QVBoxLayout()
        stretch.addStretch()
        self.template_layout.addLayout(stretch, 2, 0)

    def load_for_template(self, template: GroundObjectTemplate) -> None:
        self.template = template

        # Clean the current grid
        for id in range(self.template_grid.count()):
            self.template_grid.itemAt(id).widget().deleteLater()

        for g_id, group in enumerate(template.groups):
            group_row = QGroundObjectGroupTemplate(g_id, group)
            group_row.group_template_changed.connect(self.group_template_changed)
            self.template_grid.addWidget(group_row)

        self.update_price()

    def group_template_changed(self, group_template: GroupTemplate) -> None:
        self.update_price()

    def update_price(self) -> None:
        price = "$" + str(self.template.estimated_price_for(self.ground_object))
        self.buy_button.setText(f"Buy [{price}M][-${self.current_group_value}M]")

    def buy_group(self):
        if not self.template:
            return
        groups = self.generate_groups()

        price = 0
        for group in groups:
            for unit in group.units:
                if unit.unit_type:
                    price += unit.unit_type.price

        price -= self.current_group_value

        if price > self.game.blue.budget:
            self.error_money()
            self.close()
            return
        else:
            self.game.blue.budget -= price

        self.ground_object.groups = groups

        # Replan redfor missions
        self.game.initialize_turn(for_red=True, for_blue=False)

        GameUpdateSignal.get_instance().updateGame(self.game)

    def error_money(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Not enough money to buy these units !")
        msg.setWindowTitle("Not enough money")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.exec_()
        self.close()

    def generate_groups(self) -> list[GroundGroup]:
        go = self.template.generate(
            self.ground_object.name,
            PointWithHeading.from_point(
                self.ground_object.position, self.ground_object.heading
            ),
            self.ground_object.control_point,
            self.game,
        )
        return go.groups


class QGroundObjectBuyMenu(QDialog):
    template_changed_signal = Signal(GroundObjectTemplate)

    def __init__(
        self,
        parent,
        ground_object: TheaterGroundObject,
        game: Game,
        current_group_value: int,
    ):
        super(QGroundObjectBuyMenu, self).__init__(parent)

        self.setMinimumWidth(350)

        self.setWindowTitle("Buy ground object @ " + ground_object.obj_name)
        self.setWindowIcon(EVENT_ICONS["capture"])

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.unit_group_selector = QComboBox()
        self.template_selector = QComboBox()
        self.template_selector.setEnabled(False)

        # Get the templates and fill the combobox
        template_sub_category = None
        tasks = []
        if isinstance(ground_object, SamGroundObject):
            role = GroupRole.AntiAir
        elif isinstance(ground_object, VehicleGroupGroundObject):
            role = GroupRole.GroundForce
        elif isinstance(ground_object, EwrGroundObject):
            role = GroupRole.AntiAir
            tasks.append(GroupTask.EWR)
        else:
            raise RuntimeError

        if not tasks:
            tasks = ROLE_TASKINGS[role]

        for unit_group in game.blue.faction.groups_for_role_and_tasks(role, tasks):
            self.unit_group_selector.addItem(unit_group.name, userData=unit_group)

        self.template_selector.currentIndexChanged.connect(self.template_changed)
        self.unit_group_selector.currentIndexChanged.connect(self.unit_group_changed)

        template_selector_layout = QGridLayout()
        template_selector_layout.addWidget(QLabel("UnitGroup :"), 0, 0, Qt.AlignLeft)
        template_selector_layout.addWidget(
            self.unit_group_selector, 0, 1, alignment=Qt.AlignRight
        )
        template_selector_layout.addWidget(QLabel("Template :"), 1, 0, Qt.AlignLeft)
        template_selector_layout.addWidget(
            self.template_selector, 1, 1, alignment=Qt.AlignRight
        )
        self.mainLayout.addLayout(template_selector_layout, 0, 0)

        self.template_layout = QGroundObjectTemplateLayout(
            game, ground_object, self.template_changed_signal, current_group_value
        )
        self.mainLayout.addWidget(self.template_layout, 1, 0)
        self.setLayout(self.mainLayout)

        # Update UI
        self.unit_group_changed()

    def unit_group_changed(self) -> None:
        unit_group = self.unit_group_selector.itemData(
            self.unit_group_selector.currentIndex()
        )
        self.template_selector.clear()
        if unit_group.templates:
            for template in unit_group.templates:
                self.template_selector.addItem(template.name, userData=template)
        # Enable if more than one template is available
        self.template_selector.setEnabled(len(unit_group.templates) > 1)

    def template_changed(self):
        template = self.template_selector.itemData(
            self.template_selector.currentIndex()
        )
        if template is not None:
            self.template_changed_signal.emit(template)
