from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton

from game import Game
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.widgets.QTurnCounter import QTurnCounter

import qt_ui.uiconstants as CONST

class QTopPanel(QFrame):

    def __init__(self, game: Game):
        super(QTopPanel, self).__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):

        self.turnCounter = QTurnCounter()
        self.turnCounter.setCurrentTurn(self.game.turn, self.game.current_day)

        self.budgetBox = QBudgetBox()
        self.budgetBox.setBudget(self.game.budget, self.game.budget_reward_amount)

        self.passTurn = QPushButton("Pass Turn")
        self.passTurn.setIcon(CONST.ICONS["PassTurn"])
        self.passTurn.setProperty("style", "btn-primary")

        self.layout = QHBoxLayout()
        self.layout.addStretch(1)
        self.layout.addWidget(self.turnCounter)
        self.layout.addWidget(self.budgetBox)
        self.layout.addWidget(self.passTurn)
        self.setLayout(self.layout)