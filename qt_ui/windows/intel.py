from PySide2.QtWidgets import (
    QDialog,
    QGroupBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from game.game import Game
from qt_ui.uiconstants import ICONS
from qt_ui.windows.finances.QFinancesMenu import FinancesLayout


class EconomyIntelBox(QGroupBox):
    def __init__(self, game: Game) -> None:
        super().__init__("Economy")

        widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)

        scrolling_layout = QVBoxLayout()
        widget.setLayout(scrolling_layout)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        scrolling_layout.addLayout(FinancesLayout(game, player=False))


class IntelWindow(QDialog):

    def __init__(self, game: Game):
        super().__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Intelligence")
        self.setWindowIcon(ICONS["Statistics"])
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(EconomyIntelBox(game), stretch=1)
