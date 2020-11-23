from typing import List, Optional

from PySide2.QtWidgets import (
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
)

import qt_ui.uiconstants as CONST
from game import Game
from game.event.airwar import AirWarEvent
from gen.ato import Package
from gen.flights.traveltime import TotEstimator
from qt_ui.models import GameModel
from qt_ui.widgets.QBudgetBox import QBudgetBox
from qt_ui.widgets.QFactionsInfos import QFactionsInfos
from qt_ui.widgets.QTurnCounter import QTurnCounter
from qt_ui.widgets.clientslots import MaxPlayerCount
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.QWaitingForMissionResultWindow import \
    QWaitingForMissionResultWindow
from qt_ui.windows.settings.QSettingsWindow import QSettingsWindow
from qt_ui.windows.stats.QStatsWindow import QStatsWindow


class QTopPanel(QFrame):

    def __init__(self, game_model: GameModel):
        super(QTopPanel, self).__init__()
        self.game_model = game_model
        self.setMaximumHeight(70)
        self.init_ui()
        GameUpdateSignal.get_instance().gameupdated.connect(self.setGame)
        GameUpdateSignal.get_instance().budgetupdated.connect(self.budget_update)

    @property
    def game(self) -> Optional[Game]:
        return self.game_model.game

    def init_ui(self):

        self.turnCounter = QTurnCounter()
        self.budgetBox = QBudgetBox(self.game)

        self.passTurnButton = QPushButton("Pass Turn")
        self.passTurnButton.setIcon(CONST.ICONS["PassTurn"])
        self.passTurnButton.setProperty("style", "btn-primary")
        self.passTurnButton.clicked.connect(self.passTurn)
        if not self.game:
            self.passTurnButton.setEnabled(False)

        self.proceedButton = QPushButton("Take off")
        self.proceedButton.setIcon(CONST.ICONS["Proceed"])
        self.proceedButton.setProperty("style", "start-button")
        self.proceedButton.clicked.connect(self.launch_mission)
        if not self.game or self.game.turn == 0:
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
        self.proceedBoxLayout.addLayout(
            MaxPlayerCount(self.game_model.ato_model))
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

    def setGame(self, game: Optional[Game]):
        if game is None:
            return

        self.turnCounter.setCurrentTurn(game.turn, game.conditions)
        self.budgetBox.setGame(game)
        self.factionsInfos.setGame(game)

        self.passTurnButton.setEnabled(True)

        if game and game.turn == 0:
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

    def negative_start_packages(self) -> List[Package]:
        packages = []
        for package in self.game_model.ato_model.ato.packages:
            if not package.flights:
                continue
            estimator = TotEstimator(package)
            for flight in package.flights:
                if estimator.mission_start_time(flight).total_seconds() < 0:
                    packages.append(package)
                    break
        return packages

    @staticmethod
    def fix_tots(packages: List[Package]) -> None:
        for package in packages:
            estimator = TotEstimator(package)
            package.time_over_target = estimator.earliest_tot()

    def ato_has_clients(self) -> bool:
        for package in self.game.blue_ato.packages:
            for flight in package.flights:
                if flight.client_count > 0:
                    return True
        return False

    def confirm_no_client_launch(self) -> bool:
        result = QMessageBox.question(
            self,
            "Continue without client slots?",
            ("No client slots have been created for players. Continuing will "
             "allow the AI to perform the mission, but players will be unable "
             "to participate.<br />"
             "<br />"
             "To add client slots for players, select a package from the "
             "Packages panel on the left of the main window, and then a flight "
             "from the Flights panel below the Packages panel. The edit button "
             "below the Flights panel will allow you to edit the number of "
             "client slots in the flight. Each client slot allows one player.<br />"
             "<br />Click 'Yes' to continue with an AI only mission"
             "<br />Click 'No' if you'd like to make more changes."),
            QMessageBox.No,
            QMessageBox.Yes
        )
        return result == QMessageBox.Yes

    def confirm_negative_start_time(self,
                                    negative_starts: List[Package]) -> bool:
        formatted = '<br />'.join(
            [f"{p.primary_task.name} {p.target.name}" for p in negative_starts]
        )
        mbox = QMessageBox(
            QMessageBox.Question,
            "Continue with past start times?",
            ("Some flights in the following packages have start times set "
             "earlier than mission start time:<br />"
             "<br />"
             f"{formatted}<br />"
             "<br />"
             "Flight start times are estimated based on the package TOT, so it "
             "is possible that not all flights will be able to reach the "
             "target area at their assigned times.<br />"
             "<br />"
             "You can either continue with the mission as planned, with the "
             "misplanned flights potentially flying too fast and/or missing "
             "their rendezvous; automatically fix negative TOTs; or cancel "
             "mission start and fix the packages manually."),
            parent=self
        )
        auto = mbox.addButton("Fix TOTs automatically", QMessageBox.ActionRole)
        ignore = mbox.addButton("Continue without fixing",
                                QMessageBox.DestructiveRole)
        cancel = mbox.addButton(QMessageBox.Cancel)
        mbox.setEscapeButton(cancel)
        mbox.exec_()
        clicked = mbox.clickedButton()
        if clicked == auto:
            self.fix_tots(negative_starts)
            return True
        elif clicked == ignore:
            return True
        return False

    def launch_mission(self):
        """Finishes planning and waits for mission completion."""
        if not self.ato_has_clients() and not self.confirm_no_client_launch():
            return

        negative_starts = self.negative_start_packages()
        if negative_starts:
            if not self.confirm_negative_start_time(negative_starts):
                return
        closest_cps = self.game.theater.closest_opposing_control_points()
        game_event = AirWarEvent(
            self.game,
            closest_cps[0],
            closest_cps[1],
            self.game.theater.controlpoints[0].position,
            self.game.player_name,
            self.game.enemy_name)

        unit_map = self.game.initiate_event(game_event)
        waiting = QWaitingForMissionResultWindow(game_event, self.game,
                                                 unit_map)
        waiting.show()

    def budget_update(self, game:Game):
        self.budgetBox.setGame(game)
