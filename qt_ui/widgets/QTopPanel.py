from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QMessageBox

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

        self.passTurnButton = QPushButton("Pass Turn")
        self.passTurnButton.setIcon(CONST.ICONS["PassTurn"])
        self.passTurnButton.setProperty("style", "btn-primary")
        self.passTurnButton.clicked.connect(self.passTurn)

        self.submenus = QVBoxLayout()
        self.settings = QPushButton("Settings")
        self.settings.setIcon(CONST.ICONS["Settings"])
        self.settings.setProperty("style", "btn-primary")
        self.settings.clicked.connect(self.openSettings)

        self.statistics = QPushButton("Statistics")
        self.statistics.setIcon(CONST.ICONS["Statistics"])
        self.statistics.setProperty("style", "btn-primary")
        self.statistics.clicked.connect(self.openStatisticsWindow)

        self.submenus.addWidget(self.settings)
        self.submenus.addWidget(self.statistics)

        self.layout = QHBoxLayout()
        self.layout.addStretch(1)
        self.layout.addLayout(self.submenus)
        self.layout.addWidget(self.turnCounter)
        self.layout.addWidget(self.budgetBox)
        self.layout.addWidget(self.passTurnButton)
        self.setLayout(self.layout)

    def setGame(self, game:Game):
        self.game = game
        self.turnCounter.setCurrentTurn(self.game.turn, self.game.current_day)
        self.budgetBox.setBudget(self.game.budget, self.game.budget_reward_amount)

    def openSettings(self):
        QMessageBox.information(self, "Settings", "Todo open game settings")

    def openStatisticsWindow(self):
        QMessageBox.information(self, "Stats", "Todo open stats window")

    def passTurn(self):
        self.game.pass_turn()
        self.setGame(self.game)