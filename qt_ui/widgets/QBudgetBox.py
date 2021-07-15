from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QPushButton

import qt_ui.uiconstants as CONST
from game import Game
from game.income import Income
from qt_ui.windows.finances.QFinancesMenu import QFinancesMenu


class QBudgetBox(QGroupBox):
    """
    UI Component to display current budget and player's money
    """

    def __init__(self, game: Game):
        super(QBudgetBox, self).__init__("Budget")

        self.game = game

        self.finances = QPushButton()
        self.finances.setDisabled(True)
        self.finances.setProperty("style", "btn-primary")
        self.finances.setIcon(CONST.ICONS["Money"])
        self.finances.clicked.connect(self.openFinances)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.finances)
        self.setLayout(self.layout)

    def setBudget(self, budget, reward):
        """
        Set the money amount to display
        :param budget: Current money available
        :param reward: Planned reward for next turn
        """
        self.finances.setText(
            str(round(budget, 2)) + "M (+" + str(round(reward, 2)) + "M)"
        )

    def setGame(self, game):
        if game is None:
            return

        self.game = game
        self.setBudget(self.game.blue.budget, Income(self.game, player=True).total)
        self.finances.setEnabled(True)

    def openFinances(self):
        self.subwindow = QFinancesMenu(self.game)
        self.subwindow.show()
