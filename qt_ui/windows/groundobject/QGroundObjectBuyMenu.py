import logging
from dataclasses import dataclass, field
from typing import Type

from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QCheckBox,
)
from dcs.unittype import UnitType

from game import Game
from game.armedforces.forcegroup import ForceGroup
from game.data.groups import GroupRole, GroupTask
from game.point_with_heading import PointWithHeading
from game.theater import TheaterGroundObject
from game.theater.theatergroundobject import (
    VehicleGroupGroundObject,
    SamGroundObject,
    EwrGroundObject,
)
from game.theater.theatergroup import TheaterGroup
from game.layout.layout import (
    TheaterLayout,
    GroupLayout,
)
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal


@dataclass
class QGroupLayout:
    layout: GroupLayout
    dcs_unit_type: Type[UnitType]
    amount: int
    unit_price: int
    enabled: bool = True

    @property
    def price(self) -> int:
        return self.amount * self.unit_price if self.enabled else 0


@dataclass
class QLayout:
    layout: TheaterLayout
    force_group: ForceGroup
    group_layouts: list[QGroupLayout] = field(default_factory=list)

    @property
    def price(self) -> int:
        return sum(group.price for group in self.group_layouts)


class QGroundObjectGroupTemplate(QGroupBox):
    group_template_changed = Signal()

    def __init__(
        self, group_id: int, force_group: ForceGroup, group_layout: GroupLayout
    ) -> None:
        super().__init__(f"{group_id + 1}: {group_layout.name}")
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.amount_selector = QSpinBox()
        self.unit_selector = QComboBox()
        self.group_selector = QCheckBox()

        # Add all possible units with the price
        for unit_type in force_group.unit_types_for_group(group_layout):
            self.unit_selector.addItem(
                f"{unit_type.name} [${unit_type.price}M]",
                userData=(unit_type.dcs_unit_type, unit_type.price),
            )
        # Add all possible statics with price = 0
        for static_type in force_group.statics_for_group(group_layout):
            self.unit_selector.addItem(
                f"{static_type} (Static)", userData=(static_type, 0)
            )
        self.unit_selector.setEnabled(self.unit_selector.count() > 1)
        self.grid_layout.addWidget(self.unit_selector, 0, 0, alignment=Qt.AlignRight)
        self.grid_layout.addWidget(self.amount_selector, 0, 1, alignment=Qt.AlignRight)

        unit_type, price = self.unit_selector.itemData(
            self.unit_selector.currentIndex()
        )

        self.group_layout = QGroupLayout(
            group_layout, unit_type, group_layout.unit_counter, price
        )

        self.group_selector.setChecked(self.group_layout.enabled)
        self.group_selector.setEnabled(self.group_layout.layout.optional)

        self.amount_selector.setMinimum(1)
        self.amount_selector.setMaximum(self.group_layout.layout.max_size)
        self.amount_selector.setValue(self.group_layout.amount)
        self.amount_selector.setEnabled(self.group_layout.layout.max_size > 1)

        self.grid_layout.addWidget(self.group_selector, 0, 2, alignment=Qt.AlignRight)

        self.amount_selector.valueChanged.connect(self.on_group_changed)
        self.unit_selector.currentIndexChanged.connect(self.on_group_changed)
        self.group_selector.stateChanged.connect(self.on_group_changed)

    def on_group_changed(self) -> None:
        self.group_layout.enabled = self.group_selector.isChecked()
        unit_type, price = self.unit_selector.itemData(
            self.unit_selector.currentIndex()
        )
        self.group_layout.dcs_unit_type = unit_type
        self.group_layout.unit_price = price
        self.group_layout.amount = self.amount_selector.value()
        self.group_template_changed.emit()


class QGroundObjectTemplateLayout(QGroupBox):
    def __init__(
        self,
        game: Game,
        ground_object: TheaterGroundObject,
        layout: QLayout,
        layout_changed_signal: Signal(QLayout),
        current_group_value: int,
    ):
        super().__init__("Groups:")
        # Connect to the signal to handle template updates
        self.game = game
        self.ground_object = ground_object
        self.layout_changed_signal = layout_changed_signal
        self.layout_model = layout
        self.layout_changed_signal.connect(self.load_for_layout)

        self.current_group_value = current_group_value

        self.buy_button = QPushButton("Buy")
        self.buy_button.setEnabled(False)
        self.buy_button.clicked.connect(self.buy_group)

        self.template_layout = QGridLayout()
        self.setLayout(self.template_layout)

        self.template_grid = QGridLayout()
        self.template_layout.addLayout(self.template_grid, 0, 0, 1, 2)
        self.template_layout.addWidget(self.buy_button, 1, 1)
        stretch = QVBoxLayout()
        stretch.addStretch()
        self.template_layout.addLayout(stretch, 2, 0)

        # Load Layout
        self.load_for_layout(self.layout_model)

    def load_for_layout(self, layout: QLayout) -> None:
        self.layout_model = layout
        # Clean the current grid
        for id in range(self.template_grid.count()):
            self.template_grid.itemAt(id).widget().deleteLater()
        for g_id, layout_group in enumerate(self.layout_model.layout.groups):
            group_row = QGroundObjectGroupTemplate(
                g_id, self.layout_model.force_group, layout_group
            )
            self.layout_model.group_layouts.append(group_row.group_layout)
            group_row.group_template_changed.connect(self.group_template_changed)
            self.template_grid.addWidget(group_row)

        self.group_template_changed()

    def group_template_changed(self) -> None:
        price = self.layout_model.price
        self.buy_button.setText(f"Buy [${price}M][-${self.current_group_value}M]")
        self.buy_button.setEnabled(price <= self.game.blue.budget)
        if self.buy_button.isEnabled():
            self.buy_button.setToolTip("Buy the group")
        else:
            self.buy_button.setToolTip("Not enough money to buy this group")

    def buy_group(self):
        if not self.layout:
            raise RuntimeError("No template selected. GroundObject can not be bought.")

        price = self.layout_model.price
        if price > self.game.blue.budget:
            # Somethin went wrong. Buy button should be disabled!
            logging.error("Not enough money to buy the group")
            return
        self.game.blue.budget -= price - self.current_group_value
        self.ground_object.groups = self.generate_groups()

        # Replan redfor missions
        self.game.initialize_turn(for_red=True, for_blue=False)
        GameUpdateSignal.get_instance().updateGame(self.game)

    def generate_groups(self) -> list[TheaterGroup]:
        go = self.layout_model.layout.create_ground_object(
            self.ground_object.name,
            PointWithHeading.from_point(
                self.ground_object.position, self.ground_object.heading
            ),
            self.ground_object.control_point,
        )

        for group in self.layout_model.group_layouts:
            self.layout_model.force_group.create_theater_group_for_tgo(
                go,
                group.layout,
                self.ground_object.name,
                self.game,
                group.dcs_unit_type,  # Forced Type
                group.amount,  # Forced Amount
            )

        return go.groups


class QGroundObjectBuyMenu(QDialog):
    layout_changed_signal = Signal(QLayout)

    def __init__(
        self,
        parent,
        ground_object: TheaterGroundObject,
        game: Game,
        current_group_value: int,
    ):
        super().__init__(parent)

        self.setMinimumWidth(350)

        self.setWindowTitle("Buy ground object @ " + ground_object.obj_name)
        self.setWindowIcon(EVENT_ICONS["capture"])

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.force_group_selector = QComboBox()
        self.layout_selector = QComboBox()
        self.layout_selector.setEnabled(False)

        # Get the layouts and fill the combobox
        tasks = []
        if isinstance(ground_object, SamGroundObject):
            role = GroupRole.AIR_DEFENSE
        elif isinstance(ground_object, VehicleGroupGroundObject):
            role = GroupRole.GROUND_FORCE
        elif isinstance(ground_object, EwrGroundObject):
            role = GroupRole.AIR_DEFENSE
            tasks.append(GroupTask.EARLY_WARNING_RADAR)
        else:
            raise NotImplementedError(f"Unhandled TGO type {ground_object.__class__}")

        if not tasks:
            tasks = role.tasks

        for group in game.blue.armed_forces.groups_for_tasks(tasks):
            self.force_group_selector.addItem(group.name, userData=group)
        self.force_group_selector.setEnabled(self.force_group_selector.count() > 1)

        force_group = self.force_group_selector.itemData(
            self.force_group_selector.currentIndex()
        )

        for layout in force_group.layouts:
            self.layout_selector.addItem(layout.name, userData=layout)

        selected_template = self.layout_selector.itemData(
            self.layout_selector.currentIndex()
        )

        self.layout_model = QLayout(selected_template, force_group)

        self.layout_selector.currentIndexChanged.connect(self.layout_changed)
        self.force_group_selector.currentIndexChanged.connect(self.force_group_changed)

        template_selector_layout = QGridLayout()
        template_selector_layout.addWidget(
            QLabel("Armed Forces Group:"), 0, 0, Qt.AlignLeft
        )
        template_selector_layout.addWidget(
            self.force_group_selector, 0, 1, alignment=Qt.AlignRight
        )
        template_selector_layout.addWidget(QLabel("Layout:"), 1, 0, Qt.AlignLeft)
        template_selector_layout.addWidget(
            self.layout_selector, 1, 1, alignment=Qt.AlignRight
        )
        self.mainLayout.addLayout(template_selector_layout, 0, 0)

        self.template_layout = QGroundObjectTemplateLayout(
            game,
            ground_object,
            self.layout_model,
            self.layout_changed_signal,
            current_group_value,
        )
        self.mainLayout.addWidget(self.template_layout, 1, 0)
        self.setLayout(self.mainLayout)

    def force_group_changed(self) -> None:
        # Prevent ComboBox from firing change Events
        self.layout_selector.blockSignals(True)
        unit_group = self.force_group_selector.itemData(
            self.force_group_selector.currentIndex()
        )
        self.layout_selector.clear()
        for layout in unit_group.layouts:
            self.layout_selector.addItem(layout.name, userData=layout)
        # Enable if more than one template is available
        self.layout_selector.setEnabled(len(unit_group.layouts) > 1)
        # Enable Combobox Signals again
        self.layout_selector.blockSignals(False)
        self.layout_changed()

    def layout_changed(self):
        self.layout()
        self.layout_model.layout = self.layout_selector.itemData(
            self.layout_selector.currentIndex()
        )
        self.layout_model.force_group = self.force_group_selector.itemData(
            self.force_group_selector.currentIndex()
        )
        self.layout_model.group_layouts = []
        self.layout_changed_signal.emit(self.layout_model)
