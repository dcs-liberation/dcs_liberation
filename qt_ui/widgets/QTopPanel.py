from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout

from game import Game
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.windows.stats.QStatsWindow import QStatsWindow
from qt_ui.widgets.QTurnCounter import QTurnCounter

import qt_ui.uiconstants as CONST
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.mission.QMissionPlanning import QMissionPlanning
from qt_ui.windows.settings.QSettingsWindow import QSettingsWindow


class QTopPanel(QFrame):

    def __init__(self, game: Game):
        super(QTopPanel, self).__init__()
        self.game = game
        self.init_ui()
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)

    def init_ui(self):

        self.turnCounter = QTurnCounter()
        self.budgetBox = QBudgetBox()


        self.passTurnButton = QPushButton("Pass Turn")
        self.passTurnButton.setIcon(CONST.ICONS["PassTurn"])
        self.passTurnButton.setProperty("style", "btn-primary")
        self.passTurnButton.clicked.connect(self.passTurn)

        self.proceedButton = QPushButton("Proceed")
        self.proceedButton.setIcon(CONST.ICONS["PassTurn"])
        self.proceedButton.setProperty("style", "btn-primary")
        self.proceedButton.clicked.connect(self.proceed)

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
        self.layout.addWidget(self.proceedButton)
        self.setLayout(self.layout)

    def setGame(self, game:Game):
        self.game = game
        if game is not None:
            self.turnCounter.setCurrentTurn(self.game.turn, self.game.current_day)
            self.budgetBox.setBudget(self.game.budget, self.game.budget_reward_amount)

    def openSettings(self):
        self.subwindow = QSettingsWindow(self.game)
        self.subwindow.show()

    def openStatisticsWindow(self):
        self.subwindow = QStatsWindow(self.game)
        self.subwindow.show()

    def passTurn(self):
        self.game.pass_turn()
        GameUpdateSignal.get_instance().updateGame(self.game)

    def proceed(self):
        self.subwindow = QMissionPlanning(self.game)
        self.subwindow.show()