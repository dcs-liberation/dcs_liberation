from typing import Optional, Callable, Iterable

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
    QItemSelection,
    Signal,
)
from PySide2.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide2.QtWidgets import (
    QDialog,
    QListView,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QWidget,
    QScrollArea,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QHBoxLayout,
    QStackedLayout,
    QTabWidget,
    QComboBox,
    QPushButton,
    QGridLayout,
)

from game import Game
from game.dcs.aircrafttype import AircraftType
from game.squadrons import AirWing, Pilot, Squadron
from game.theater import ControlPoint, ConflictTheater
from gen.flights.flight import FlightType
from qt_ui.uiconstants import AIRCRAFT_ICONS


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
    def __init__(self, squadron: Squadron, theater: ConflictTheater) -> None:
        super().__init__()
        self.setCheckable(True)
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
    def __init__(self, squadrons: list[Squadron], theater: ConflictTheater) -> None:
        super().__init__()
        self.squadron_configs = []
        for squadron in squadrons:
            squadron_config = SquadronConfigurationBox(squadron, theater)
            self.squadron_configs.append(squadron_config)
            self.addWidget(squadron_config)

    def apply(self) -> list[Squadron]:
        keep_squadrons = []
        for squadron_config in self.squadron_configs:
            if squadron_config.isChecked():
                keep_squadrons.append(squadron_config.apply())
        return keep_squadrons


class AircraftSquadronsPage(QWidget):
    def __init__(self, squadrons: list[Squadron], theater: ConflictTheater) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.squadrons_config = SquadronConfigurationLayout(squadrons, theater)

        scrolling_widget = QWidget()
        scrolling_widget.setLayout(self.squadrons_config)

        scrolling_area = QScrollArea()
        scrolling_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrolling_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrolling_area.setWidgetResizable(True)
        scrolling_area.setWidget(scrolling_widget)

        layout.addWidget(scrolling_area)

    def apply(self) -> list[Squadron]:
        return self.squadrons_config.apply()


class AircraftSquadronsPanel(QStackedLayout):
    def __init__(self, air_wing: AirWing, theater: ConflictTheater) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.squadrons_pages: dict[AircraftType, AircraftSquadronsPage] = {}
        for aircraft, squadrons in self.air_wing.squadrons.items():
            page = AircraftSquadronsPage(squadrons, theater)
            self.addWidget(page)
            self.squadrons_pages[aircraft] = page

    def apply(self) -> None:
        for aircraft, page in self.squadrons_pages.items():
            self.air_wing.squadrons[aircraft] = page.apply()


class AircraftTypeList(QListView):
    page_index_changed = Signal(int)

    def __init__(self, air_wing: AirWing) -> None:
        super().__init__()
        self.setIconSize(QSize(91, 24))
        self.setMinimumWidth(300)

        self.air_wing = air_wing

        model = QStandardItemModel(self)
        self.setModel(model)

        self.selectionModel().setCurrentIndex(
            model.index(0, 0), QItemSelectionModel.Select
        )
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

        for aircraft in self.air_wing.squadrons:
            aircraft_item = QStandardItem(aircraft.name)
            icon = self.icon_for(aircraft)
            if icon is not None:
                aircraft_item.setIcon(icon)
            aircraft_item.setEditable(False)
            aircraft_item.setSelectable(True)
            model.appendRow(aircraft_item)

        air_wing.subscribe(self.handleChanges)

    def handleChanges(self, event):
        if event.type == "remove_aircraft_type":
            # self.air_wing = event.obj
            model = QStandardItemModel(self)
            for aircraft in self.air_wing.squadrons:
                aircraft_item = QStandardItem(aircraft.name)
                icon = self.icon_for(aircraft)
                if icon is not None:
                    aircraft_item.setIcon(icon)
                aircraft_item.setEditable(False)
                aircraft_item.setSelectable(True)
                model.appendRow(aircraft_item)

            self.setModel(model)
            self.selectionModel().clearSelection
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
            print("Removing..." + aircraftName)
            to_remove = None
            for type in self.air_wing.squadrons:
                if str(type) == aircraftName:
                    to_remove = type
            if to_remove != None:
                self.air_wing.remove_aircraft_type(to_remove)
            else:
                raise RuntimeError("No aircraft was selected for removal")

    def addAircraftType(self) -> None:
        print()

    @staticmethod
    def icon_for(aircraft: AircraftType) -> Optional[QIcon]:
        name = aircraft.dcs_id
        if name in AIRCRAFT_ICONS:
            return QIcon(AIRCRAFT_ICONS[name])
        return None


class AirWingConfigurationTab(QWidget):
    def __init__(self, air_wing: AirWing, theater: ConflictTheater) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.theater = theater
        layout = QGridLayout()
        self.setLayout(layout)

        type_list = AircraftTypeList(self.air_wing)
        type_list.page_index_changed.connect(self.on_aircraft_changed)
        layout.addWidget(type_list, 1, 1, 1, 2)

        add_button = QPushButton("Add aircraft type")
        add_button.clicked.connect(lambda state: type_list.addAircraftType())
        layout.addWidget(add_button, 2, 1, 1, 1)

        remove_button = QPushButton("Remove selected")
        remove_button.clicked.connect(lambda state: type_list.deleteSelectedType())
        layout.addWidget(remove_button, 2, 2, 1, 1)

        self.squadrons_panel = AircraftSquadronsPanel(self.air_wing, self.theater)
        layout.addLayout(self.squadrons_panel, 1, 3, 2, 1)

        air_wing.subscribe(self.handleChanges)

    def apply(self) -> None:
        self.squadrons_panel.apply()

    def on_aircraft_changed(self, index: QModelIndex) -> None:
        self.squadrons_panel.setCurrentIndex(index)

    def handleChanges(self, event) -> None:
        if event.type == "remove_aircraft_type":
            self.squadrons_panel = AircraftSquadronsPanel(self.air_wing, self.theater)
            self.layout().addLayout(self.squadrons_panel, 1, 3, 2, 1)
        self.update()


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
            coalition_tab = AirWingConfigurationTab(coalition.air_wing, game.theater)
            name = "Blue" if coalition.player else "Red"
            tab_widget.addTab(coalition_tab, name)
            self.tabs.append(coalition_tab)

    def reject(self) -> None:
        for tab in self.tabs:
            tab.apply()
        super().reject()
