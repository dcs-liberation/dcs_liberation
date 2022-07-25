from typing import Iterable, Iterator, Optional

from PySide2.QtCore import (
    QItemSelection,
    QItemSelectionModel,
    QSize,
    Qt,
    Signal,
)
from PySide2.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedLayout,
    QTabWidget,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from game import Game
from game.ato.flighttype import FlightType
from game.coalition import Coalition
from game.dcs.aircrafttype import AircraftType
from game.squadrons import AirWing, Pilot, Squadron
from game.squadrons.squadrondef import SquadronDef
from game.theater import ConflictTheater, ControlPoint
from qt_ui.uiconstants import AIRCRAFT_ICONS, ICONS


class QMissionType:
    def __init__(
        self, mission_type: FlightType, allowed: bool, auto_assignable: bool
    ) -> None:
        self.flight_type = mission_type
        self.allowed_checkbox = QCheckBox()
        self.allowed_checkbox.setChecked(allowed)
        self.allowed_checkbox.toggled.connect(self.update_auto_assignable)
        self.auto_assignable_checkbox = QCheckBox()
        self.auto_assignable_checkbox.setEnabled(allowed)
        self.auto_assignable_checkbox.setChecked(auto_assignable)

    def update_auto_assignable(self, checked: bool) -> None:
        self.auto_assignable_checkbox.setEnabled(checked)
        if not checked:
            self.auto_assignable_checkbox.setChecked(False)

    @property
    def allowed(self) -> bool:
        return self.allowed_checkbox.isChecked()

    @property
    def auto_assignable(self) -> bool:
        return self.auto_assignable_checkbox.isChecked()


class MissionTypeControls(QGridLayout):
    def __init__(self, squadron: Squadron) -> None:
        super().__init__()
        self.squadron = squadron
        self.mission_types: list[QMissionType] = []

        self.addWidget(QLabel("Mission Type"), 0, 0)
        self.addWidget(QLabel("Allow"), 0, 1)
        self.addWidget(QLabel("Auto-Assign"), 0, 2)

        for i, task in enumerate(FlightType):
            if task is FlightType.FERRY:
                # Not plannable so just skip it.
                continue
            allowed = task in squadron.mission_types
            auto_assignable = task in squadron.auto_assignable_mission_types
            mission_type = QMissionType(task, allowed, auto_assignable)
            self.mission_types.append(mission_type)

            self.addWidget(QLabel(task.value), i + 1, 0)
            self.addWidget(mission_type.allowed_checkbox, i + 1, 1)
            self.addWidget(mission_type.auto_assignable_checkbox, i + 1, 2)

    @property
    def allowed_mission_types(self) -> Iterator[FlightType]:
        for mission_type in self.mission_types:
            if mission_type.allowed:
                yield mission_type.flight_type

    @property
    def auto_assignable_mission_types(self) -> Iterator[FlightType]:
        for mission_type in self.mission_types:
            if mission_type.auto_assignable:
                yield mission_type.flight_type


class SquadronBaseSelector(QComboBox):
    """A combo box for selecting a squadrons home air base.

    The combo box will automatically be populated with all air bases compatible with the
    squadron.
    """

    def __init__(
        self,
        bases: Iterable[ControlPoint],
        selected_base: Optional[ControlPoint],
        aircraft_type: Optional[AircraftType],
    ) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.bases = list(bases)
        self.set_aircraft_type(aircraft_type)

        if selected_base:
            self.setCurrentText(selected_base.name)
        # TODO can we get a prefered base if none is selected?

    def set_aircraft_type(self, aircraft_type: Optional[AircraftType]):
        self.clear()
        if aircraft_type:
            for base in self.bases:
                if not base.can_operate(aircraft_type):
                    continue
                self.addItem(base.name, base)
            self.model().sort(0)
            self.setEnabled(True)
        else:
            self.addItem("Select aircraft type first", None)
            self.setEnabled(False)
        self.update()


class SquadronConfigurationBox(QGroupBox):
    remove_squadron_signal = Signal(Squadron)

    def __init__(self, squadron: Squadron, theater: ConflictTheater) -> None:
        super().__init__()
        self.squadron = squadron

        columns = QHBoxLayout()
        self.setLayout(columns)

        left_column = QVBoxLayout()
        columns.addLayout(left_column)

        left_column.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit(squadron.name)
        self.name_edit.textChanged.connect(lambda x: self.reset_title())
        left_column.addWidget(self.name_edit)

        self.reset_title()

        nickname_edit_layout = QGridLayout()
        left_column.addLayout(nickname_edit_layout)

        nickname_edit_layout.addWidget(QLabel("Nickname:"), 0, 0, 1, 2)
        self.nickname_edit = QLineEdit(squadron.nickname)
        nickname_edit_layout.addWidget(self.nickname_edit, 1, 0, Qt.AlignTop)
        reroll_nickname_button = QToolButton()
        reroll_nickname_button.setIcon(QIcon(ICONS["Reload"]))
        reroll_nickname_button.setToolTip("Re-roll nickname")
        reroll_nickname_button.clicked.connect(self.reroll_nickname)
        nickname_edit_layout.addWidget(reroll_nickname_button, 1, 1, Qt.AlignTop)

        left_column.addWidget(QLabel("Base:"))
        self.base_selector = SquadronBaseSelector(
            theater.control_points_for(squadron.player),
            squadron.location,
            squadron.aircraft,
        )
        left_column.addWidget(self.base_selector)

        if not squadron.player and squadron.aircraft.flyable:
            player_label = QLabel("Player slots not available for opfor")
        elif not squadron.aircraft.flyable:
            player_label = QLabel("Player slots not available for non-flyable aircraft")
        else:
            player_label = QLabel(
                "Players (one per line, leave empty for an AI-only squadron):"
            )
        left_column.addWidget(player_label)

        players = [p for p in squadron.pilot_pool if p.player]
        for player in players:
            squadron.pilot_pool.remove(player)
        if not squadron.player:
            players = []
        self.player_list = QTextEdit("<br />".join(p.name for p in players))
        self.player_list.setAcceptRichText(False)
        self.player_list.setEnabled(squadron.player and squadron.aircraft.flyable)
        left_column.addWidget(self.player_list)
        delete_button = QPushButton("Remove Squadron")
        delete_button.setMaximumWidth(140)
        delete_button.clicked.connect(self.remove_from_squadron_config)
        left_column.addWidget(delete_button)
        left_column.addStretch()

        right_column = QVBoxLayout()
        self.mission_types = MissionTypeControls(squadron)
        right_column.addLayout(self.mission_types)
        right_column.addStretch()
        columns.addLayout(right_column)

    def remove_from_squadron_config(self) -> None:
        self.remove_squadron_signal.emit(self.squadron)

    def reset_title(self) -> None:
        self.setTitle(f"{self.name_edit.text()} - {self.squadron.aircraft}")

    def reroll_nickname(self) -> None:
        self.nickname_edit.setText(
            self.squadron.coalition.air_wing.squadron_def_generator.random_nickname()
        )

    def apply(self) -> Squadron:
        self.squadron.name = self.name_edit.text()
        self.squadron.nickname = self.nickname_edit.text()
        base = self.base_selector.currentData()
        if base is None:
            raise RuntimeError("Base cannot be none")
        self.squadron.assign_to_base(base)

        player_names = self.player_list.toPlainText().splitlines()
        # Prepend player pilots so they get set active first.
        self.squadron.pilot_pool = [
            Pilot(n, player=True) for n in player_names
        ] + self.squadron.pilot_pool
        # Set the allowed mission types
        self.squadron.set_allowed_mission_types(
            set(self.mission_types.allowed_mission_types)
        )
        # Also update the auto assignable mission types
        self.squadron.set_auto_assignable_mission_types(
            set(self.mission_types.auto_assignable_mission_types)
        )
        return self.squadron


class SquadronConfigurationLayout(QVBoxLayout):
    config_changed = Signal(AircraftType)

    def __init__(self, squadrons: list[Squadron], theater: ConflictTheater) -> None:
        super().__init__()
        self.squadron_configs = []
        self.theater = theater
        for squadron in squadrons:
            self.add_squadron(squadron)

    def apply(self) -> list[Squadron]:
        keep_squadrons = []
        for squadron_config in self.squadron_configs:
            keep_squadrons.append(squadron_config.apply())
        return keep_squadrons

    def remove_squadron(self, squadron: Squadron) -> None:
        for squadron_config in self.squadron_configs:
            if squadron_config.squadron == squadron:
                squadron_config.deleteLater()
                self.squadron_configs.remove(squadron_config)
                squadron.coalition.air_wing.unclaim_squadron_def(squadron)
                self.update()
                self.config_changed.emit(squadron.aircraft)
                return

    def add_squadron(self, squadron: Squadron) -> None:
        squadron_config = SquadronConfigurationBox(squadron, self.theater)
        squadron_config.remove_squadron_signal.connect(self.remove_squadron)
        self.squadron_configs.append(squadron_config)
        self.addWidget(squadron_config)


class AircraftSquadronsPage(QWidget):
    remove_squadron_page = Signal(AircraftType)

    def __init__(self, squadrons: list[Squadron], theater: ConflictTheater) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.squadrons_config = SquadronConfigurationLayout(squadrons, theater)
        self.squadrons_config.config_changed.connect(self.on_squadron_config_changed)

        scrolling_widget = QWidget()
        scrolling_widget.setLayout(self.squadrons_config)

        scrolling_area = QScrollArea()
        scrolling_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrolling_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrolling_area.setWidgetResizable(True)
        scrolling_area.setWidget(scrolling_widget)

        layout.addWidget(scrolling_area)

    def on_squadron_config_changed(self, aircraft_type: AircraftType):
        if len(self.squadrons_config.squadron_configs) == 0:
            self.remove_squadron_page.emit(aircraft_type)

    def add_squadron_to_page(self, squadron: Squadron):
        self.squadrons_config.add_squadron(squadron)

    def apply(self) -> list[Squadron]:
        return self.squadrons_config.apply()


class AircraftSquadronsPanel(QStackedLayout):
    page_removed = Signal(AircraftType)

    def __init__(self, air_wing: AirWing, theater: ConflictTheater) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.theater = theater
        self.squadrons_pages: dict[AircraftType, AircraftSquadronsPage] = {}
        for aircraft, squadrons in self.air_wing.squadrons.items():
            self.new_page_for_type(aircraft, squadrons)

    def remove_page_for_type(self, aircraft_type: AircraftType):
        page = self.squadrons_pages[aircraft_type]
        self.removeWidget(page)
        page.deleteLater()
        self.squadrons_pages.pop(aircraft_type)
        self.page_removed.emit(aircraft_type)
        self.update()

    def new_page_for_type(
        self, aircraft_type: AircraftType, squadrons: list[Squadron]
    ) -> None:
        page = AircraftSquadronsPage(squadrons, self.theater)
        page.remove_squadron_page.connect(self.remove_page_for_type)
        self.addWidget(page)
        self.squadrons_pages[aircraft_type] = page

    def add_squadron_to_panel(self, squadron: Squadron):
        # Find existing page or add new one
        if squadron.aircraft in self.squadrons_pages:
            page = self.squadrons_pages[squadron.aircraft]
            page.add_squadron_to_page(squadron)
        else:
            self.new_page_for_type(squadron.aircraft, [squadron])

        self.update()

    def apply(self) -> None:
        self.air_wing.squadrons = {}
        for aircraft, page in self.squadrons_pages.items():
            self.air_wing.squadrons[aircraft] = page.apply()

    def revert(self) -> None:
        for _, page in self.squadrons_pages.items():
            self.removeWidget(page)
        self.squadrons_pages: dict[AircraftType, AircraftSquadronsPage] = {}
        for aircraft, squadrons in self.air_wing.squadrons.items():
            self.new_page_for_type(aircraft, squadrons)
        self.update()


class AircraftTypeList(QListView):
    page_index_changed = Signal(int)

    def __init__(self, air_wing: AirWing) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.setIconSize(QSize(91, 24))
        self.setMinimumWidth(300)

        self.item_model = QStandardItemModel(self)
        self.setModel(self.item_model)

        self.selectionModel().setCurrentIndex(
            self.item_model.index(0, 0), QItemSelectionModel.Select
        )
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        for aircraft in air_wing.squadrons:
            self.add_aircraft_type(aircraft)

    def remove_aircraft_type(self, aircraft: AircraftType):
        for item in self.item_model.findItems(aircraft.name):
            self.item_model.removeRow(item.row())
        self.page_index_changed.emit(self.selectionModel().currentIndex().row())

    def add_aircraft_type(self, aircraft: AircraftType):
        aircraft_item = QStandardItem(aircraft.name)
        icon = self.icon_for(aircraft)
        if icon is not None:
            aircraft_item.setIcon(icon)
        aircraft_item.setEditable(False)
        aircraft_item.setSelectable(True)
        self.item_model.appendRow(aircraft_item)

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        indexes = selected.indexes()
        if len(indexes) > 1:
            raise RuntimeError("Aircraft list should not allow multi-selection")
        if not indexes:
            return
        self.page_index_changed.emit(indexes[0].row())

    @staticmethod
    def icon_for(aircraft: AircraftType) -> Optional[QIcon]:
        name = aircraft.dcs_id
        if name in AIRCRAFT_ICONS:
            return QIcon(AIRCRAFT_ICONS[name])
        return None

    def revert(self) -> None:
        self.item_model.clear()
        for aircraft in self.air_wing.squadrons:
            self.add_aircraft_type(aircraft)
        self.update()


class AirWingConfigurationTab(QWidget):
    def __init__(self, coalition: Coalition, game: Game) -> None:
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)
        self.game = game
        self.coalition = coalition

        self.type_list = AircraftTypeList(coalition.air_wing)

        layout.addWidget(self.type_list, 1, 1, 1, 2)

        add_button = QPushButton("Add Squadron")
        add_button.clicked.connect(lambda state: self.add_squadron())
        layout.addWidget(add_button, 2, 1, 1, 1)

        self.squadrons_panel = AircraftSquadronsPanel(coalition.air_wing, game.theater)
        self.squadrons_panel.page_removed.connect(self.type_list.remove_aircraft_type)
        layout.addLayout(self.squadrons_panel, 1, 3, 2, 1)

        self.type_list.page_index_changed.connect(self.squadrons_panel.setCurrentIndex)

    def add_squadron(self) -> None:
        selected_aircraft = None
        if self.type_list.selectionModel().currentIndex().row() >= 0:
            selected_aircraft = self.type_list.item_model.item(
                self.type_list.selectionModel().currentIndex().row()
            ).text()

        bases = list(self.game.theater.control_points_for(self.coalition.player))

        # List of all Aircrafts possible to operate with the given bases
        possible_aircrafts = [
            aircraft
            for aircraft in self.coalition.faction.aircrafts
            if any(base.can_operate(aircraft) for base in bases)
        ]

        popup = SquadronConfigPopup(
            selected_aircraft,
            possible_aircrafts,
            bases,
            self.coalition.air_wing.squadron_defs,
        )
        if popup.exec_() != QDialog.Accepted:
            return

        selected_type = popup.aircraft_type_selector.currentData()
        selected_base = popup.squadron_base_selector.currentData()
        selected_def = popup.squadron_def_selector.currentData()

        # Let user choose the preset or generate one
        squadron_def = (
            selected_def
            or self.coalition.air_wing.squadron_def_generator.generate_for_aircraft(
                selected_type
            )
        )

        squadron = Squadron.create_from(
            squadron_def, selected_base, self.coalition, self.game
        )

        # Add Squadron
        if not self.type_list.item_model.findItems(selected_type.name):
            self.type_list.add_aircraft_type(selected_type)
            # TODO Select the newly added type
        self.squadrons_panel.add_squadron_to_panel(squadron)
        self.update()

    def apply(self) -> None:
        self.squadrons_panel.apply()

    def revert(self) -> None:
        self.type_list.revert()
        self.squadrons_panel.revert()
        self.update()


class AirWingConfigurationDialog(QDialog):
    """Dialog window for air wing configuration."""

    def __init__(self, game: Game, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(1024, 768)
        self.setWindowTitle(f"Air Wing Configuration")
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        doc_label = QLabel(
            "Use this opportunity to customize the squadrons available to your "
            "coalition. <strong>This is your only opportunity to make changes.</strong>"
            "<br /><br />"
            "To accept your changes and continue, close this window."
        )

        layout.addWidget(doc_label)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.tabs = []
        for coalition in game.coalitions:
            coalition_tab = AirWingConfigurationTab(coalition, game)
            name = "Blue" if coalition.player else "Red"
            self.tab_widget.addTab(coalition_tab, name)
            self.tabs.append(coalition_tab)

        buttons_layout = QHBoxLayout()
        apply_button = QPushButton("Accept Changes && Start Campaign")
        apply_button.setProperty("style", "btn-accept")
        apply_button.clicked.connect(lambda state: self.accept())
        discard_button = QPushButton("Reset Changes")
        discard_button.setProperty("style", "btn-danger")
        discard_button.clicked.connect(lambda state: self.revert())
        buttons_layout.addWidget(discard_button)
        buttons_layout.addWidget(apply_button)
        layout.addLayout(buttons_layout)

    def revert(self) -> None:
        for tab in self.tabs:
            tab.revert()

    def accept(self) -> None:
        for tab in self.tabs:
            tab.apply()
        super().accept()

    def reject(self) -> None:
        result = QMessageBox.information(
            None,
            "Discard changes?",
            "Are you sure you want to discard your changes and start the campaign?",
            QMessageBox.Yes,
            QMessageBox.No,
        )
        if result == QMessageBox.No:
            return
        super().reject()


class SquadronAircraftTypeSelector(QComboBox):
    def __init__(
        self, types: list[AircraftType], selected_aircraft: Optional[str]
    ) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToContents)

        for type in sorted(types, key=lambda type: type.name):
            self.addItem(type.name, type)

        if selected_aircraft:
            self.setCurrentText(selected_aircraft)


class SquadronDefSelector(QComboBox):
    def __init__(
        self,
        squadron_defs: dict[AircraftType, list[SquadronDef]],
        aircraft: Optional[AircraftType],
    ) -> None:
        super().__init__()
        self.setSizeAdjustPolicy(self.AdjustToContents)
        self.squadron_defs = squadron_defs
        self.set_aircraft_type(aircraft)

    def set_aircraft_type(self, aircraft: Optional[AircraftType]):
        self.clear()
        self.addItem("None (Random)", None)
        if aircraft and aircraft in self.squadron_defs:
            for squadron_def in sorted(
                self.squadron_defs[aircraft], key=lambda squadron_def: squadron_def.name
            ):
                if not squadron_def.claimed:
                    squadron_name = squadron_def.name
                    if squadron_def.nickname:
                        squadron_name += " (" + squadron_def.nickname + ")"
                    self.addItem(squadron_name, squadron_def)
        self.setCurrentText("None (Random)")


class SquadronConfigPopup(QDialog):
    def __init__(
        self,
        selected_aircraft: Optional[str],
        types: list[AircraftType],
        bases: list[ControlPoint],
        squadron_defs: dict[AircraftType, list[SquadronDef]],
    ) -> None:
        super().__init__()

        self.setWindowTitle(f"Add new Squadron")

        self.column = QVBoxLayout()
        self.setLayout(self.column)

        self.bases = bases

        self.column.addWidget(QLabel("Aircraft:"))
        self.aircraft_type_selector = SquadronAircraftTypeSelector(
            types, selected_aircraft
        )
        self.aircraft_type_selector.currentIndexChanged.connect(
            self.on_aircraft_selection
        )
        self.column.addWidget(self.aircraft_type_selector)

        self.column.addWidget(QLabel("Base:"))
        self.squadron_base_selector = SquadronBaseSelector(
            bases, None, self.aircraft_type_selector.currentData()
        )
        self.column.addWidget(self.squadron_base_selector)

        self.column.addWidget(QLabel("Preset:"))
        self.squadron_def_selector = SquadronDefSelector(
            squadron_defs, self.aircraft_type_selector.currentData()
        )
        self.column.addWidget(self.squadron_def_selector)

        self.column.addStretch()

        self.button_layout = QHBoxLayout()
        self.column.addLayout(self.button_layout)

        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(lambda state: self.accept())
        self.update_accept_button()
        self.button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda state: self.reject())
        self.button_layout.addWidget(self.cancel_button)

    def update_accept_button(self) -> None:
        enabled = (
            self.aircraft_type_selector.currentData() is not None
            and self.squadron_base_selector.currentData() is not None
        )
        self.accept_button.setEnabled(enabled)

    def on_aircraft_selection(self) -> None:
        self.squadron_base_selector.set_aircraft_type(
            self.aircraft_type_selector.currentData()
        )
        self.squadron_def_selector.set_aircraft_type(
            self.aircraft_type_selector.currentData()
        )
        self.update_accept_button()
        self.update()
