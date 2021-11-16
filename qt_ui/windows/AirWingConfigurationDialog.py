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
)

from game import Game
from game.ato.flighttype import FlightType
from game.coalition import Coalition
from game.dcs.aircrafttype import AircraftType
from game.squadrons import AirWing, Pilot, Squadron
from game.theater import ConflictTheater, ControlPoint
from qt_ui.uiconstants import AIRCRAFT_ICONS

from qt_ui.windows.SquadronConfigPopup import SquadronConfigPopup


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
        self.squadron.set_allowed_mission_types(self.allowed_mission_types)


class SquadronBaseSelector(QComboBox):
    """A combo box for selecting a squadrons home air base.

    The combo box will automatically be populated with all air bases compatible with the
    squadron.
    """

    def __init__(
        self,
        bases: Iterable[ControlPoint],
        squadron: Squadron,
    ) -> None:
        super().__init__()
        self.bases = list(bases)
        self.squadron = squadron
        self.setSizeAdjustPolicy(self.AdjustToContents)

        for base in self.bases:
            if not base.can_operate(self.squadron.aircraft):
                continue
            self.addItem(base.name, base)
        self.model().sort(0)
        self.setCurrentText(self.squadron.location.name)


class SquadronConfigurationBox(QGroupBox):
    def __init__(
        self, squadron: Squadron, theater: ConflictTheater, air_wing: AirWing
    ) -> None:
        super().__init__()
        self.setCheckable(False)
        self.squadron = squadron
        self.air_wing = air_wing
        self.reset_title()

        columns = QHBoxLayout()
        self.setLayout(columns)

        left_column = QVBoxLayout()
        columns.addLayout(left_column)

        left_column.addWidget(QLabel("Name:"))
        self.name_edit = QLineEdit(squadron.name)
        self.name_edit.textChanged.connect(self.on_name_changed)
        left_column.addWidget(self.name_edit)

        left_column.addWidget(QLabel("Nickname:"))
        self.nickname_edit = QLineEdit(squadron.nickname)
        self.nickname_edit.textChanged.connect(self.on_nickname_changed)
        left_column.addWidget(self.nickname_edit)

        left_column.addWidget(QLabel("Base:"))
        self.base_selector = SquadronBaseSelector(
            theater.control_points_for(squadron.player), squadron
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
        self.player_list.textChanged.connect(self.on_pilots_changed)

        delete_button = QPushButton("Remove")
        delete_button.setMaximumWidth(80)
        delete_button.clicked.connect(
            lambda state: self.air_wing.remove_squadron(self.squadron)
        )
        left_column.addWidget(delete_button)

        left_column.addStretch()

        self.allowed_missions = AllowedMissionTypeControls(squadron)
        columns.addLayout(self.allowed_missions)

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

    def on_pilots_changed(self) -> None:
        player_names = self.player_list.toPlainText().splitlines()
        # Prepend player pilots so they get set active first.
        self.squadron.pilot_pool = [
            Pilot(n, player=True) for n in player_names
        ] + self.squadron.pilot_pool


class SquadronConfigurationLayout(QVBoxLayout):
    def __init__(
        self, squadrons: list[Squadron], theater: ConflictTheater, air_wing: AirWing
    ) -> None:
        super().__init__()
        self.theater = theater
        self.air_wing = air_wing
        self.squadron_configs: dict[Squadron, SquadronConfigurationBox] = {}
        for squadron in squadrons:
            squadron_config = SquadronConfigurationBox(
                squadron, self.theater, self.air_wing
            )
            self.squadron_configs[squadron] = squadron_config
            self.addWidget(squadron_config)

    def addSquadron(self, squadron: Squadron) -> None:
        if squadron not in self.squadron_configs:
            squadron_config = SquadronConfigurationBox(
                squadron, self.theater, self.air_wing
            )
            self.squadron_configs[squadron] = squadron_config
            self.addWidget(squadron_config)
            self.update()

    def removeSquadron(self, squadron: Squadron) -> None:
        if squadron in self.squadron_configs:
            self.removeWidget(self.squadron_configs[squadron])
            self.squadron_configs.pop(squadron)
            self.update()


class AircraftSquadronsPage(QWidget):
    def __init__(
        self, squadrons: list[Squadron], theater: ConflictTheater, air_wing: AirWing
    ) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.squadrons_config = SquadronConfigurationLayout(
            squadrons, theater, air_wing
        )

        scrolling_widget = QWidget()
        scrolling_widget.setLayout(self.squadrons_config)

        scrolling_area = QScrollArea()
        scrolling_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrolling_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrolling_area.setWidgetResizable(True)
        scrolling_area.setWidget(scrolling_widget)

        layout.addWidget(scrolling_area)

    def addSquadron(self, squadron: Squadron) -> None:
        self.squadrons_config.addSquadron(squadron)

    def removeSquadron(self, squadron: Squadron) -> None:
        self.squadrons_config.removeSquadron(squadron)


class AircraftSquadronsPanel(QStackedLayout):
    def __init__(self, air_wing: AirWing, theater: ConflictTheater) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.theater = theater
        self.air_wing.subscribe(self.handleChanges)

        self.squadrons_pages: dict[AircraftType, AircraftSquadronsPage] = {}
        for aircraft, squadrons in self.air_wing.squadrons.items():
            page = AircraftSquadronsPage(squadrons, self.theater, self.air_wing)
            self.addWidget(page)
            self.squadrons_pages[aircraft] = page

    def __del__(self) -> None:
        self.air_wing.unsubscribe(self.handleChanges)

    def handleChanges(self, event) -> None:
        if event.type == "add_aircraft_type":
            aircraft_type = event.obj
            if aircraft_type not in self.squadrons_pages:
                page = AircraftSquadronsPage(
                    self.air_wing.squadrons[aircraft_type], self.theater, self.air_wing
                )
                self.addWidget(page)
                self.squadrons_pages[aircraft_type] = page
        elif event.type == "remove_aircraft_type":
            aircraft_type = event.obj
            if aircraft_type in self.squadrons_pages:
                self.removeWidget(self.squadrons_pages[aircraft_type])
                self.squadrons_pages.pop(aircraft_type)
        elif event.type == "add_squadron":
            squadron = event.obj
            self.squadrons_pages[squadron.aircraft].addSquadron(squadron)
        elif event.type == "remove_squadron":
            squadron = event.obj
            self.squadrons_pages[squadron.aircraft].removeSquadron(squadron)
        self.update()


class AircraftTypeList(QListView):
    page_index_changed = Signal(int)

    def __init__(self, air_wing: AirWing) -> None:
        super().__init__()
        self.setIconSize(QSize(91, 24))
        self.setMinimumWidth(300)

        self.air_wing = air_wing

        self.item_model = QStandardItemModel(self)
        self.setModel(self.item_model)

        for aircraft in self.air_wing.squadrons:
            aircraft_item = QStandardItem(aircraft.name)
            icon = self.icon_for(aircraft)
            if icon is not None:
                aircraft_item.setIcon(icon)
            aircraft_item.setEditable(False)
            aircraft_item.setSelectable(True)
            self.item_model.appendRow(aircraft_item)

        self.selectionModel().setCurrentIndex(
            self.item_model.index(0, 0), QItemSelectionModel.Select
        )
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self.air_wing.subscribe(self.handleChanges)

    def __del__(self) -> None:
        self.air_wing.unsubscribe(self.handleChanges)

    def handleChanges(self, event) -> None:
        if event.type == "remove_aircraft_type":
            aircraft_type = event.obj
            items = self.item_model.findItems(aircraft_type.name)
            if len(items) == 1:
                for item in items:
                    self.item_model.takeRow(item.row())
        elif event.type == "add_aircraft_type":
            aircraft_type = event.obj
            aircraft_item = QStandardItem(aircraft_type.name)
            icon = self.icon_for(aircraft_type)
            if icon is not None:
                aircraft_item.setIcon(icon)
            aircraft_item.setEditable(False)
            aircraft_item.setSelectable(True)
            self.item_model.appendRow(aircraft_item)
        self.update()

    def on_selection_changed(
        self, selected: QItemSelection, _deselected: QItemSelection
    ) -> None:
        indexes = selected.indexes()
        if len(indexes) > 1:
            raise RuntimeError("Aircraft list should not allow multi-selection")
        if not indexes:
            return
        self.page_index_changed.emit(indexes[0].row())

    def deleteSelectedType(self) -> None:
        if self.selectionModel().currentIndex().isValid():
            aircraftName = str(self.selectionModel().currentIndex().data())
            to_remove = None
            for type in self.air_wing.squadrons:
                if str(type) == aircraftName:
                    to_remove = type
            if to_remove != None:
                self.air_wing.remove_aircraft_type(to_remove)
            else:
                raise RuntimeError("No aircraft was selected for removal")

    @staticmethod
    def icon_for(aircraft: AircraftType) -> Optional[QIcon]:
        name = aircraft.dcs_id
        if name in AIRCRAFT_ICONS:
            return QIcon(AIRCRAFT_ICONS[name])
        return None


class AirWingConfigurationTab(QWidget):
    def __init__(
        self, coalition: Coalition, theater: ConflictTheater, game: Game
    ) -> None:
        super().__init__()
        self.game = game
        self.theater = theater
        self.coalition = coalition
        self.air_wing = coalition.air_wing

        layout = QGridLayout()
        self.setLayout(layout)

        self.type_list = AircraftTypeList(self.air_wing)

        layout.addWidget(self.type_list, 1, 1, 1, 2)

        add_button = QPushButton("Add Aircraft/Squadron")
        add_button.clicked.connect(lambda state: self.addAircraftType())
        layout.addWidget(add_button, 2, 1, 1, 1)

        remove_button = QPushButton("Remove Aircraft")
        remove_button.clicked.connect(lambda state: self.type_list.deleteSelectedType())
        layout.addWidget(remove_button, 2, 2, 1, 1)

        self.squadrons_panel = AircraftSquadronsPanel(self.air_wing, self.theater)
        layout.addLayout(self.squadrons_panel, 1, 3, 2, 1)

        self.type_list.page_index_changed.connect(self.squadrons_panel.setCurrentIndex)

    def addAircraftType(self) -> None:
        SquadronConfigPopup(self.coalition, self.theater, self.game).exec_()


class AirWingConfigurationDialog(QDialog):
    """Dialog window for air wing configuration."""

    def __init__(self, game: Game, parent) -> None:
        super().__init__(parent)
        self.setMinimumSize(500, 800)
        self.setWindowTitle(f"Air Wing Configuration")
        # TODO: self.setWindowIcon()

        layout = QVBoxLayout()
        self.setLayout(layout)

        doc_url = (
            "https://github.com/dcs-liberation/dcs_liberation/wiki/Squadrons-and-pilots"
        )
        doc_label = QLabel(
            "Use this opportunity to customize the squadrons available to your "
            "coalition. <strong>This is your only opportunity to make changes.</strong>"
            "<br /><br />"
            "To accept your changes and continue, close this window.<br />"
            "<br />"
            "To remove a squadron from the game, uncheck the box in the title. New "
            "squadrons cannot be added via the UI at this time. To add a custom "
            "squadron,<br />"
            f'see <a style="color:#ffffff" href="{doc_url}">the wiki</a>.'
        )

        doc_label.setOpenExternalLinks(True)
        layout.addWidget(doc_label)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        self.tabs = []
        for coalition in game.coalitions:
            coalition_tab = AirWingConfigurationTab(coalition, game.theater, game)
            name = "Blue" if coalition.player else "Red"
            tab_widget.addTab(coalition_tab, name)
            self.tabs.append(coalition_tab)

    def reject(self) -> None:
        super().reject()
