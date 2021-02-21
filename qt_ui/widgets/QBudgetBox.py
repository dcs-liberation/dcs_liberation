from PySide2.QtWidgets import QLabel, QHBoxLayout, QGroupBox, QPushButton

import qt_ui.uiconstants as CONST
from game.income import Income
from qt_ui.windows.finances.QFinancesMenu import QFinancesMenu


class QBudgetBox(QGroupBox):
    """
    UI Component to display current budget and player's money
    """

    def __init__(self, game):
        super(QBudgetBox, self).__init__("Budget")

        self.game = game
        self.money_icon = QLabel()
        self.money_icon.setPixmap(CONST.ICONS["Money"])
        self.money_amount = QLabel()

        self.finances = QPushButton("Details")
        self.finances.setDisabled(True)
        self.finances.setProperty("style", "btn-primary")
        self.finances.clicked.connect(self.openFinances)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.money_icon)
        self.layout.addWidget(self.money_amount)
        self.layout.addWidget(self.finances)
        self.setLayout(self.layout)

    def setBudget(self, budget, reward):
        """
        Set the money amount to display
        :param budget: Current money available
        :param reward: Planned reward for next turn
        """
        self.money_amount.setText(
            str(round(budget, 2)) + "M (+" + str(round(reward, 2)) + "M)"
        )

    def setGame(self, game):
        if game is None:
            return

        self.game = game
        self.setBudget(self.game.budget, Income(self.game, player=True).total)
        self.finances.setEnabled(True)

    def openFinances(self):
        self.subwindow = QFinancesMenu(self.game)
        self.subwindow.show()
