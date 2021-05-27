import itertools
import logging
from collections import defaultdict
from typing import Optional, Callable, Iterator

from PySide2.QtCore import (
    QItemSelectionModel,
    QModelIndex,
    QSize,
    Qt,
)
from PySide2.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QListView,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QLabel,
    QWidget,
    QScrollArea,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QHBoxLayout,
)

from game import Game
from game.squadrons import Squadron, AirWing, Pilot
from gen.flights.flight import FlightType
from qt_ui.models import AirWingModel, SquadronModel
from qt_ui.windows.AirWingDialog import SquadronDelegate
from qt_ui.windows.SquadronDialog import SquadronDialog


class SquadronList(QListView):
    """List view for displaying the air wing's squadrons."""

    def __init__(self, air_wing_model: AirWingModel) -> None:
        super().__init__()
        self.air_wing_model = air_wing_model
        self.dialog: Optional[SquadronDialog] = None

        self.setIconSize(QSize(91, 24))
        self.setItemDelegate(SquadronDelegate(self.air_wing_model))
        self.setModel(self.air_wing_model)
        self.selectionModel().setCurrentIndex(
            self.air_wing_model.index(0, 0, QModelIndex()), QItemSelectionModel.Select
        )

        # self.setIconSize(QSize(91, 24))
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index: QModelIndex) -> None:
        if not index.isValid():
            return
        self.dialog = SquadronDialog(
            SquadronModel(self.air_wing_model.squadron_at_index(index)), self
        )
        self.dialog.show()


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


class SquadronConfigurationBox(QGroupBox):
    def __init__(self, squadron: Squadron) -> None:
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

        left_column.addWidget(
            QLabel("Players (one per line, leave empty for an AI-only squadron):")
        )
        players = [p for p in squadron.available_pilots if p.player]
        for player in players:
            squadron.available_pilots.remove(player)
        self.player_list = QTextEdit("<br />".join(p.name for p in players))
        self.player_list.setAcceptRichText(False)
        left_column.addWidget(self.player_list)

        left_column.addStretch()

        self.allowed_missions = AllowedMissionTypeControls(squadron)
        columns.addLayout(self.allowed_missions)

    def on_name_changed(self, text: str) -> None:
        self.squadron.name = text
        self.reset_title()

    def on_nickname_changed(self, text: str) -> None:
        self.squadron.nickname = text

    def reset_title(self) -> None:
        self.setTitle(f"{self.squadron.name} - {self.squadron.aircraft}")

    def apply(self) -> Squadron:
        player_names = self.player_list.toPlainText().splitlines()
        # Prepend player pilots so they get set active first.
        self.squadron.pilot_pool = [
            Pilot(n, player=True) for n in player_names
        ] + self.squadron.pilot_pool
        self.squadron.mission_types = tuple(self.allowed_missions.allowed_mission_types)
        return self.squadron


class AirWingConfigurationLayout(QVBoxLayout):
    def __init__(self, air_wing: AirWing) -> None:
        super().__init__()
        self.air_wing = air_wing
        self.squadron_configs = []

        doc_url = (
            "https://github.com/dcs-liberation/dcs_liberation/wiki/Squadrons-and-pilots"
        )
        doc_label = QLabel(
            "Use this opportunity to customize the squadrons available to your "
            "coalition. <strong>This is your<br />"
            "only opportunity to make changes.</strong><br />"
            "<br />"
            "To accept your changes and continue, close this window.<br />"
            "<br />"
            "To remove a squadron from the game, uncheck the box in the title. New "
            "squadrons cannot<br />"
            "be added via the UI at this time. To add a custom squadron, see "
            f'<a style="color:#ffffff" href="{doc_url}">the wiki</a>.'
        )

        doc_label.setOpenExternalLinks(True)
        self.addWidget(doc_label)
        for squadron in self.air_wing.iter_squadrons():
            squadron_config = SquadronConfigurationBox(squadron)
            self.squadron_configs.append(squadron_config)
            self.addWidget(squadron_config)

    def apply(self) -> None:
        keep_squadrons = defaultdict(list)
        for squadron_config in self.squadron_configs:
            if squadron_config.isChecked():
                squadron = squadron_config.apply()
                keep_squadrons[squadron.aircraft].append(squadron)
        self.air_wing.squadrons = keep_squadrons


class AirWingConfigurationDialog(QDialog):
    """Dialog window for air wing configuration."""

    def __init__(self, game: Game, parent) -> None:
        super().__init__(parent)
        self.air_wing = game.blue.air_wing

        self.setMinimumSize(500, 800)
        self.setWindowTitle(f"Air Wing Configuration")
        # TODO: self.setWindowIcon()

        self.air_wing_config = AirWingConfigurationLayout(self.air_wing)

        scrolling_layout = QVBoxLayout()
        scrolling_widget = QWidget()
        scrolling_widget.setLayout(self.air_wing_config)

        scrolling_area = QScrollArea()
        scrolling_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrolling_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrolling_area.setWidgetResizable(True)
        scrolling_area.setWidget(scrolling_widget)

        scrolling_layout.addWidget(scrolling_area)
        self.setLayout(scrolling_layout)

    def reject(self) -> None:
        self.air_wing_config.apply()
        super().reject()
