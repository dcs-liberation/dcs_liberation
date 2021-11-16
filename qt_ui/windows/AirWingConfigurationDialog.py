from typing import Callable, Iterable, Optional

from PySide2.QtCore import (
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
    Signal,
)
from PySide2.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QScrollArea,
    QStackedLayout,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QPushButton,
    QGridLayout,
    QToolButton,
)

from game import Game
from game.ato.flighttype import FlightType
from game.coalition import Coalition
from game.dcs.aircrafttype import AircraftType
from game.squadrons import AirWing, Pilot, Squadron
from game.squadrons.squadrondef import SquadronDef
from game.theater import ConflictTheater, ControlPoint
from qt_ui.uiconstants import AIRCRAFT_ICONS, ICONS


class AllowedMissionTypeControls(QVBoxLayout):
    def __init__(self, squadron: Squadron) -> None:
        super().__init__()
        self.squadron = squadron
        self.allowed_mission_types = set()

        self.addWidget(QLabel("Allowed mission types"))

        def make_callback(toggled_task: FlightType) -> Callable[[bool], None]:
            def callback(checked: bool) -> None:
                self.on_toggled(toggled_task, checked)

            return callback

        for task in FlightType:
            if task is FlightType.FERRY:
                # Not plannable so just skip it.
                continue
            enabled = task in squadron.mission_types
            if enabled:
                self.allowed_mission_types.add(task)
            checkbox = QCheckBox(text=task.value)
            checkbox.setChecked(enabled)
            checkbox.toggled.connect(make_callback(task))
            self.addWidget(checkbox)

        self.addStretch()

    def on_toggled(self, task: FlightType, checked: bool) -> None:
        if checked:
            self.allowed_mission_types.add(task)
        else:
            self.allowed_mission_types.remove(task)


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
        self.reset_title()

        columns = QHBoxLayout()
        self.setLayout(columns)

        left_column = QVBoxLayout()
        columns.addLayout(left_column)

        left_column.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit(squadron.name)
        self.name_edit.textChanged.connect(self.on_name_changed)
        left_column.addWidget(self.name_edit)

        nickname_edit_layout = QGridLayout()
        left_column.addLayout(nickname_edit_layout)

        nickname_edit_layout.addWidget(QLabel("Nickname:"), 0, 0, 1, 2)
        self.nickname_edit = QLineEdit(squadron.nickname)
        self.nickname_edit.textChanged.connect(self.on_nickname_changed)
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
        self.base_selector.currentIndexChanged.connect(self.on_base_changed)
        left_column.addWidget(self.base_selector)

        if squadron.player:
            player_label = QLabel(
                "Players (one per line, leave empty for an AI-only squadron):"
            )
        else:
            player_label = QLabel("Player slots not available for opfor")
        left_column.addWidget(player_label)

        players = [p for p in squadron.pilot_pool if p.player]
        for player in players:
            squadron.pilot_pool.remove(player)
        if not squadron.player:
            players = []
        self.player_list = QTextEdit("<br />".join(p.name for p in players))
        self.player_list.setAcceptRichText(False)
        self.player_list.setEnabled(squadron.player)
        left_column.addWidget(self.player_list)
        delete_button = QPushButton("Remove Squadron")
        delete_button.setMaximumWidth(140)
        delete_button.clicked.connect(self.remove_from_squadron_config)
        left_column.addWidget(delete_button)
        left_column.addStretch()

        self.allowed_missions = AllowedMissionTypeControls(squadron)
        columns.addLayout(self.allowed_missions)

    def remove_from_squadron_config(self) -> None:
        self.remove_squadron_signal.emit(self.squadron)

    def on_name_changed(self, text: str) -> None:
        self.squadron.name = text
        self.reset_title()

    def on_nickname_changed(self, text: str) -> None:
        self.squadron.nickname = text

    def on_base_changed(self, index: int) -> None:
        base = self.base_selector.itemData(index)
        if base is None:
            raise RuntimeError("Base cannot be none")
        self.squadron.assign_to_base(base)

    def reset_title(self) -> None:
        self.setTitle(f"{self.squadron.name} - {self.squadron.aircraft}")

    def reroll_nickname(self) -> None:
        self.nickname_edit.setText(
            self.squadron.coalition.air_wing.squadron_def_generator.random_nickname()
        )

    def apply(self) -> Squadron:
        player_names = self.player_list.toPlainText().splitlines()
        # Prepend player pilots so they get set active first.
        self.squadron.pilot_pool = [
            Pilot(n, player=True) for n in player_names
        ] + self.squadron.pilot_pool
        self.squadron.set_allowed_mission_types(
            self.allowed_missions.allowed_mission_types
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


class AircraftTypeList(QListView):
    page_index_changed = Signal(int)

    def __init__(self, air_wing: AirWing) -> None:
        super().__init__()
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

        popup = SquadronConfigPopup(
            selected_aircraft,
            self.coalition.faction.aircrafts,
            list(self.game.theater.control_points_for(self.coalition.player)),
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


class AirWingConfigurationDialog(QDialog):
    """Dialog window for air wing configuration."""

    def __init__(self, game: Game, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(500, 800)
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

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        self.tabs = []
        for coalition in game.coalitions:
            coalition_tab = AirWingConfigurationTab(coalition, game)
            name = "Blue" if coalition.player else "Red"
            tab_widget.addTab(coalition_tab, name)
            self.tabs.append(coalition_tab)

    def reject(self) -> None:
        for tab in self.tabs:
            tab.apply()
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
        self.button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(lambda state: self.reject())
        self.button_layout.addWidget(self.cancel_button)

    def on_aircraft_selection(self) -> None:
        self.squadron_base_selector.set_aircraft_type(
            self.aircraft_type_selector.currentData()
        )
        self.squadron_def_selector.set_aircraft_type(
            self.aircraft_type_selector.currentData()
        )
        self.update()
