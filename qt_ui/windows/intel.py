import itertools
from typing import Optional

from PySide2.QtWidgets import (
    QCheckBox,
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLayout,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from game.game import Game
from qt_ui.uiconstants import ICONS
from qt_ui.windows.finances.QFinancesMenu import FinancesLayout


class ScrollingFrame(QFrame):
    def __init__(self) -> None:
        super().__init__()

        widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)

        self.scrolling_layout = QVBoxLayout()
        widget.setLayout(self.scrolling_layout)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

    def addWidget(self, widget: QWidget, *args, **kwargs) -> None:
        self.scrolling_layout.addWidget(widget, *args, **kwargs)

    def addLayout(self, layout: QLayout, *args, **kwargs) -> None:
        self.scrolling_layout.addLayout(layout, *args, **kwargs)


class EconomyIntelTab(ScrollingFrame):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()
        self.addLayout(FinancesLayout(game, player=player, total_at_top=True))


class IntelTableLayout(QGridLayout):
    def __init__(self) -> None:
        super().__init__()
        self.row = itertools.count(0)

    def add_header(self, text: str) -> None:
        self.addWidget(QLabel(f"<b>{text}</b>"), next(self.row), 0)

    def add_spacer(self) -> None:
        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Expanding),
            next(self.row),
            0,
        )

    def add_row(self, text: str, count: Optional[int] = None) -> None:
        row = next(self.row)
        self.addWidget(QLabel(text), row, 0)
        if count is not None:  # optional count for blank rows
            self.addWidget(QLabel(str(count)), row, 1)


class AircraftIntelLayout(IntelTableLayout):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()

        total = 0
        for control_point in game.theater.control_points_for(player):
            allocation = control_point.allocated_aircraft()
            base_total = allocation.total_present
            total += base_total
            if not base_total:
                continue

            self.add_header(f"{control_point.name} ({base_total})")
            for airframe in sorted(allocation.present, key=lambda k: k.name):
                count = allocation.present[airframe]
                if not count:
                    continue
                self.add_row(f"    {airframe.name}", count)
            self.add_row("")

        self.add_row("<b>Total</b>", total)
        self.add_spacer()


class AircraftIntelTab(ScrollingFrame):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()
        self.addLayout(AircraftIntelLayout(game, player=player))


class ArmyIntelLayout(IntelTableLayout):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()

        total = 0
        for control_point in game.theater.control_points_for(player):
            base = control_point.base
            total += base.total_armor
            if not base.total_armor:
                continue

            self.add_header(f"{control_point.name} ({base.total_armor})")
            for vehicle in sorted(base.armor, key=lambda k: k.name):
                count = base.armor[vehicle]
                if not count:
                    continue
                self.add_row(f"    {vehicle.name}", count)
            self.add_row("")

        self.add_row("<b>Total</b>", total)
        self.add_spacer()


class ArmyIntelTab(ScrollingFrame):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()
        self.addLayout(ArmyIntelLayout(game, player=player))


class IntelTabs(QTabWidget):
    def __init__(self, game: Game, player: bool):
        super().__init__()

        self.addTab(EconomyIntelTab(game, player), "Economy")
        self.addTab(AircraftIntelTab(game, player), "Air forces")
        self.addTab(ArmyIntelTab(game, player), "Ground forces")


class IntelWindow(QDialog):
    def __init__(self, game: Game):
        super().__init__()

        self.game = game
        self.player = True
        self.setModal(True)
        self.setWindowTitle("Intelligence")
        self.setWindowIcon(ICONS["Statistics"])
        self.setMinimumSize(600, 500)
        self.selected_intel_tab = 0

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.refresh_layout()

    def on_faction_changed(self) -> None:
        self.player = not self.player
        self.refresh_layout()

    def refresh_layout(self) -> None:

        # Clear the existing layout
        if self.layout():
            idx = 0
            while child := self.layout().itemAt(idx):
                self.layout().removeItem(child)

        # Add the new layout
        own_faction = QCheckBox("Enemy Info")
        own_faction.setChecked(not self.player)
        own_faction.stateChanged.connect(self.on_faction_changed)

        intel_tabs = IntelTabs(self.game, self.player)
        intel_tabs.currentChanged.connect(self.on_tab_changed)

        if self.selected_intel_tab:
            intel_tabs.setCurrentIndex(self.selected_intel_tab)

        self.layout().addWidget(own_faction)
        self.layout().addWidget(intel_tabs, stretch=1)

    def on_tab_changed(self, idx: int) -> None:
        self.selected_intel_tab = idx
