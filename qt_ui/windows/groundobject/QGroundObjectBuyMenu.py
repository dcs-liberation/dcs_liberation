import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Type

from PySide2.QtCore import Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from dcs.unittype import UnitType

from game import Game
from game.armedforces.forcegroup import ForceGroup
from game.data.groups import GroupRole, GroupTask
from game.layout.layout import (
    LayoutException,
    TgoLayout,
    TgoLayoutUnitGroup,
)
from game.theater import TheaterGroundObject
from game.theater.theatergroundobject import (
    EwrGroundObject,
    SamGroundObject,
    VehicleGroupGroundObject,
)
from qt_ui.uiconstants import EVENT_ICONS


@dataclass
class QTgoLayoutGroup:
    layout: TgoLayoutUnitGroup
    dcs_unit_type: Type[UnitType]
    amount: int
    unit_price: int
    enabled: bool = True

    @property
    def price(self) -> int:
        return self.amount * self.unit_price if self.enabled else 0


@dataclass
class QTgoLayout:
    layout: TgoLayout
    force_group: ForceGroup
    groups: dict[str, list[QTgoLayoutGroup]] = field(default_factory=dict)

    @property
    def price(self) -> int:
        return sum(group.price for groups in self.groups.values() for group in groups)


class QTgoLayoutGroupRow(QWidget):
    group_template_changed = Signal()

    def __init__(self, force_group: ForceGroup, group: TgoLayoutUnitGroup) -> None:
        super().__init__()
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.grid_layout.setColumnStretch(0, 100)
        self.amount_selector = QSpinBox()
        self.unit_selector = QComboBox()
        self.unit_selector.setMinimumWidth(250)
        self.group_selector = QCheckBox()

        # Add all possible units with the price
        for unit_type in force_group.unit_types_for_group(group):
            self.unit_selector.addItem(
                f"{unit_type.name} [${unit_type.price}M]",
                userData=(unit_type.dcs_unit_type, unit_type.price),
            )
        # Add all possible statics with price = 0
        for static_type in force_group.statics_for_group(group):
            self.unit_selector.addItem(
                f"{static_type} (Static)", userData=(static_type, 0)
            )

        if self.unit_selector.count() == 0:
            raise LayoutException("No units available for the TgoLayoutGroup")

        self.unit_selector.adjustSize()
        self.unit_selector.setEnabled(self.unit_selector.count() > 1)
        self.grid_layout.addWidget(self.unit_selector, 0, 0, alignment=Qt.AlignRight)
        self.grid_layout.addWidget(self.amount_selector, 0, 1, alignment=Qt.AlignRight)

        dcs_unit_type, price = self.unit_selector.itemData(
            self.unit_selector.currentIndex()
        )

        self.group_layout = QTgoLayoutGroup(
            group, dcs_unit_type, group.group_size, price
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
    close_dialog_signal = Signal()

    def __init__(
        self,
        game: Game,
        ground_object: TheaterGroundObject,
        layout: QTgoLayout,
        layout_changed_signal: Signal(QTgoLayout),
        current_group_value: int,
    ):
        super().__init__()
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

    def load_for_layout(self, layout: QTgoLayout) -> None:
        self.layout_model = layout
        # Clean the current grid
        self.layout_model.groups = defaultdict(list)
        for id in range(self.template_grid.count()):
            self.template_grid.itemAt(id).widget().deleteLater()
        for group in self.layout_model.layout.groups:
            self.add_theater_group(
                group.group_name, self.layout_model.force_group, group.unit_groups
            )
        self.group_template_changed()

    @property
    def cost(self) -> int:
        return self.layout_model.price - self.current_group_value

    @property
    def affordable(self) -> bool:
        return self.cost <= self.game.blue.budget

    def add_theater_group(
        self, group_name: str, force_group: ForceGroup, groups: list[TgoLayoutUnitGroup]
    ) -> None:
        group_box = QGroupBox(group_name)
        vbox_layout = QVBoxLayout()
        for group in groups:
            try:
                group_row = QTgoLayoutGroupRow(force_group, group)
            except LayoutException:
                continue
            self.layout_model.groups[group_name].append(group_row.group_layout)
            group_row.group_template_changed.connect(self.group_template_changed)
            vbox_layout.addWidget(group_row)
        group_box.setLayout(vbox_layout)
        self.template_grid.addWidget(group_box)

    def group_template_changed(self) -> None:
        price = self.layout_model.price
        self.buy_button.setText(f"Buy [${price}M][-${self.current_group_value}M]")
        self.buy_button.setEnabled(self.affordable)
        if self.buy_button.isEnabled():
            self.buy_button.setToolTip(f"Buy the group for ${self.cost}M")
        else:
            self.buy_button.setToolTip("Not enough money to buy this group")

    def buy_group(self) -> None:
        if not self.affordable:
            # Something went wrong. Buy button should be disabled!
            logging.error("Not enough money to buy the group")
            return

        # Change the heading of the new group to head to the conflict
        self.ground_object.heading = (
            self.game.theater.heading_to_conflict_from(self.ground_object.position)
            or self.ground_object.heading
        )
        self.game.blue.budget -= self.cost
        self.ground_object.groups = []
        for group_name, groups in self.layout_model.groups.items():
            for group in groups:
                if group.enabled:
                    self.layout_model.force_group.create_theater_group_for_tgo(
                        self.ground_object,
                        group.layout,
                        f"{self.ground_object.name} ({group_name})",
                        self.game,
                        group.dcs_unit_type,  # Forced Type
                        group.amount,  # Forced Amount
                    )
        self.close_dialog_signal.emit()


class QGroundObjectBuyMenu(QDialog):
    layout_changed_signal = Signal(QTgoLayout)

    def __init__(
        self,
        parent: QWidget,
        ground_object: TheaterGroundObject,
        game: Game,
        current_group_value: int,
    ) -> None:
        super().__init__(parent)

        self.setMinimumWidth(350)

        self.setWindowTitle("Buy ground object @ " + ground_object.obj_name)
        self.setWindowIcon(EVENT_ICONS["capture"])

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)

        self.force_group_selector = QComboBox()
        self.force_group_selector.setMinimumWidth(250)
        self.layout_selector = QComboBox()
        self.layout_selector.setMinimumWidth(250)

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
        self.force_group_selector.adjustSize()
        force_group = self.force_group_selector.itemData(
            self.force_group_selector.currentIndex()
        )

        for layout in force_group.layouts:
            self.layout_selector.addItem(layout.name, userData=layout)
        self.layout_selector.adjustSize()
        self.layout_selector.setEnabled(len(force_group.layouts) > 1)
        selected_template = self.layout_selector.itemData(
            self.layout_selector.currentIndex()
        )

        self.theater_layout = QTgoLayout(selected_template, force_group)

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
            self.theater_layout,
            self.layout_changed_signal,
            current_group_value,
        )
        self.template_layout.close_dialog_signal.connect(self.close_dialog)
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
        self.layout_selector.adjustSize()
        # Enable if more than one template is available
        self.layout_selector.setEnabled(len(unit_group.layouts) > 1)
        # Enable Combobox Signals again
        self.layout_selector.blockSignals(False)
        self.layout_changed()

    def layout_changed(self) -> None:
        self.layout()
        self.theater_layout.layout = self.layout_selector.itemData(
            self.layout_selector.currentIndex()
        )
        self.theater_layout.force_group = self.force_group_selector.itemData(
            self.force_group_selector.currentIndex()
        )
        self.layout_changed_signal.emit(self.theater_layout)

    def close_dialog(self) -> None:
        self.accept()
