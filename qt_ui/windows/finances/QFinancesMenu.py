import itertools
from typing import Optional

from PySide2.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QSizePolicy,
)

import qt_ui.uiconstants as CONST
from game.game import Game
from game.income import BuildingIncome, Income
from game.theater import ControlPoint


class QHorizontalSeparationLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)


class FinancesLayout(QGridLayout):
    def __init__(self, game: Game, player: bool, total_at_top: bool = False) -> None:
        super().__init__()
        self.row = itertools.count(0)

        income = Income(game, player)

        if total_at_top:
            self.add_total(game, income, player)
            self.add_line()

        control_points = reversed(
            sorted(income.control_points, key=lambda c: c.income_per_turn)
        )
        for control_point in control_points:
            self.add_control_point(control_point)

        self.add_line()

        buildings = reversed(sorted(income.buildings, key=lambda b: b.income))
        for building in buildings:
            self.add_building(building)

        if not total_at_top:
            self.add_line()
            self.add_total(game, income, player)

    def add_total(self, game, income, player):
        self.add_row(
            middle=f"Income multiplier: {income.multiplier:.1f}",
            right=f"<b>{income.total:.1f}M</b>",
        )
        budget = game.coalition_for(player).budget
        self.add_row(middle="Balance", right=f"<b>{budget:.1f}M</b>")
        self.setRowStretch(next(self.row), 1)

    def add_row(
        self,
        left: Optional[str] = None,
        middle: Optional[str] = None,
        right: Optional[str] = None,
    ) -> None:
        if not any([left, middle, right]):
            raise ValueError

        row = next(self.row)
        if left is not None:
            self.addWidget(QLabel(left), row, 0)
        if middle is not None:
            self.addWidget(QLabel(middle), row, 1)
        if right is not None:
            self.addWidget(QLabel(right), row, 2)

    def add_control_point(self, control_point: ControlPoint) -> None:
        self.add_row(
            left=f"<b>{control_point.name}</b>",
            right=f"{control_point.income_per_turn}M",
        )

    def add_building(self, building: BuildingIncome) -> None:
        row = next(self.row)
        self.addWidget(
            QLabel(f"<b>{building.category.upper()} [{building.name}]</b>"), row, 0
        )
        self.addWidget(
            QLabel(f"{building.number} buildings x {building.income_per_building}M"),
            row,
            1,
        )
        rlabel = QLabel(f"{building.income}M")
        rlabel.setProperty("style", "green")
        self.addWidget(rlabel, row, 2)

    def add_line(self) -> None:
        self.addWidget(QHorizontalSeparationLine(), next(self.row), 0, 1, 3)


class QFinancesMenu(QDialog):
    def __init__(self, game: Game):
        super(QFinancesMenu, self).__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Finances")
        self.setWindowIcon(CONST.ICONS["Money"])
        self.setMinimumSize(450, 200)

        self.setLayout(FinancesLayout(game, player=True))
