from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QVBoxLayout, QGroupBox

from game import Game
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.widgets.QFactionsInfos import QFactionsInfos
from qt_ui.windows.finances.QFinancesMenu import QFinancesMenu
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
        self.setMaximumHeight(70)
        self.init_ui()
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)

    def init_ui(self):

        self.turnCounter = QTurnCounter()
        self.budgetBox = QBudgetBox(self.game)

        self.passTurnButton = QPushButton("Pass Turn")
        self.passTurnButton.setIcon(CONST.ICONS["PassTurn"])
        self.passTurnButton.setProperty("style", "btn-primary")
        self.passTurnButton.clicked.connect(self.passTurn)

        self.proceedButton = QPushButton("Proceed")
        self.proceedButton.setIcon(CONST.ICONS["Proceed"])
        self.proceedButton.setProperty("style", "btn-primary")
        self.proceedButton.clicked.connect(self.proceed)
        if self.game and self.game.turn == 0:
            self.proceedButton.setEnabled(False)

        self.factionsInfos = QFactionsInfos(self.game)

        self.settings = QPushButton("Settings")
        self.settings.setIcon(CONST.ICONS["Settings"])
        self.settings.setProperty("style", "btn-primary")
        self.settings.clicked.connect(self.openSettings)

        self.statistics = QPushButton("Statistics")
        self.statistics.setIcon(CONST.ICONS["Statistics"])
        self.statistics.setProperty("style", "btn-primary")
        self.statistics.clicked.connect(self.openStatisticsWindow)

        self.buttonBox = QGroupBox("Misc")
        self.buttonBoxLayout = QHBoxLayout()
        self.buttonBoxLayout.addWidget(self.settings)
        self.buttonBoxLayout.addWidget(self.statistics)
        self.buttonBox.setLayout(self.buttonBoxLayout)

        self.proceedBox = QGroupBox("Proceed")
        self.proceedBoxLayout = QHBoxLayout()
        self.proceedBoxLayout.addWidget(self.passTurnButton)
        self.proceedBoxLayout.addWidget(self.proceedButton)
        self.proceedBox.setLayout(self.proceedBoxLayout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.factionsInfos)
        self.layout.addWidget(self.turnCounter)
        self.layout.addWidget(self.budgetBox)
        self.layout.addWidget(self.buttonBox)
        self.layout.addStretch(1)
        self.layout.addWidget(self.proceedBox)

        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

    def setGame(self, game:Game):
        self.game = game
        if game is not None:
            self.turnCounter.setCurrentTurn(self.game.turn, self.game.current_day)
            self.budgetBox.setGame(self.game)
            self.factionsInfos.setGame(self.game)

            if not len(self.game.planners.keys()) == len(self.game.theater.controlpoints):
                self.proceedButton.setEnabled(False)
            else:
                self.proceedButton.setEnabled(True)

    def openSettings(self):
        self.subwindow = QSettingsWindow(self.game)
        self.subwindow.show()

    def openStatisticsWindow(self):
        self.subwindow = QStatsWindow(self.game)
        self.subwindow.show()

    def passTurn(self):
        self.game.pass_turn(no_action=True)
        GameUpdateSignal.get_instance().updateGame(self.game)
        self.proceedButton.setEnabled(True)

    def proceed(self):
        self.subwindow = QMissionPlanning(self.game)
        self.subwindow.show()