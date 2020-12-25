from PySide2.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QSizePolicy,
)

import qt_ui.uiconstants as CONST
from game.game import Game
from game.income import Income


class QHorizontalSeparationLine(QFrame):

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class FinancesLayout(QGridLayout):
    def __init__(self, game: Game, player: bool) -> None:
        super().__init__()

        income = Income(game, player)

        self.addWidget(QLabel("<b>Control Points</b>"), 0, 0)
        self.addWidget(QLabel(
            f"{len(income.control_points)} bases x {income.income_per_base}M"),
            0, 1)
        self.addWidget(QLabel(f"{income.from_bases}M"), 0, 2)

        self.addWidget(QHorizontalSeparationLine(), 1, 0, 1, 3)

        buildings = reversed(sorted(income.buildings, key=lambda b: b.income))
        row = 2
        for row, building in enumerate(buildings, row):
            self.addWidget(
                QLabel(f"<b>{building.category.upper()} [{building.name}]</b>"),
                row, 0)
            self.addWidget(QLabel(
                f"{building.number} buildings x {building.income_per_building}M"),
                row, 1)
            rlabel = QLabel(f"{building.income}M")
            rlabel.setProperty("style", "green")
            self.addWidget(rlabel, row, 2)

        self.addWidget(QHorizontalSeparationLine(), row + 1, 0, 1, 3)
        self.addWidget(QLabel(
            f"Income multiplier: {income.multiplier:.1f}"),
            row + 2, 1
        )
        self.addWidget(QLabel(f"<b>{income.total}M</b>"), row + 2, 2)

        if player:
            budget = game.budget
        else:
            budget = game.enemy_budget
        self.addWidget(QLabel(f"Balance"), row + 3, 1)
        self.addWidget(QLabel(f"<b>{budget}M</b>"), row + 3, 2)
        self.setRowStretch(row + 4, 1)


class QFinancesMenu(QDialog):

    def __init__(self, game: Game):
        super(QFinancesMenu, self).__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Finances")
        self.setWindowIcon(CONST.ICONS["Money"])
        self.setMinimumSize(450, 200)

        self.setLayout(FinancesLayout(game, player=True))
