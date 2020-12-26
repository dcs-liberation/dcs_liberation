import itertools

from PySide2.QtWidgets import (
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
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.addLayout(FinancesLayout(game, player=False))


class IntelTableLayout(QGridLayout):
    def __init__(self) -> None:
        super().__init__()
        self.row = itertools.count(0)

    def add_header(self, text: str) -> None:
        self.addWidget(QLabel(f"<b>{text}</b>"), next(self.row), 0)

    def add_spacer(self) -> None:
        self.addItem(
            QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Expanding),
            next(self.row), 0)

    def add_row(self, text: str, count: int) -> None:
        row = next(self.row)
        self.addWidget(QLabel(text), row, 0)
        self.addWidget(QLabel(str(count)), row, 1)


class AircraftIntelLayout(IntelTableLayout):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()

        total = 0
        for control_point in game.theater.control_points_for(player):
            base = control_point.base
            total += base.total_aircraft
            if not base.total_aircraft:
                continue

            self.add_header(control_point.name)
            for airframe, count in base.aircraft.items():
                if not count:
                    continue
                self.add_row(airframe.id, count)

        self.add_spacer()
        self.add_row("<b>Total</b>", total)


class AircraftIntelTab(ScrollingFrame):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.addLayout(AircraftIntelLayout(game, player=False))


class ArmyIntelLayout(IntelTableLayout):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()

        total = 0
        for control_point in game.theater.control_points_for(player):
            base = control_point.base
            total += base.total_armor
            if not base.total_armor:
                continue

            self.add_header(control_point.name)
            for vehicle, count in base.armor.items():
                if not count:
                    continue
                self.add_row(vehicle.id, count)

        self.add_spacer()
        self.add_row("<b>Total</b>", total)


class ArmyIntelTab(ScrollingFrame):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.addLayout(ArmyIntelLayout(game, player=False))


class IntelTabs(QTabWidget):

    def __init__(self, game: Game):
        super().__init__()

        self.addTab(EconomyIntelTab(game), "Economy")
        self.addTab(AircraftIntelTab(game), "Air forces")
        self.addTab(ArmyIntelTab(game), "Ground forces")


class IntelWindow(QDialog):

    def __init__(self, game: Game):
        super().__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Intelligence")
        self.setWindowIcon(ICONS["Statistics"])
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(IntelTabs(game), stretch=1)
