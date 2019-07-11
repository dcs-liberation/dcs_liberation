import os

from PySide2 import QtCore
from PySide2.QtGui import QMovie
from PySide2.QtWidgets import QLabel, QDialog, QVBoxLayout

from game.game import Event, Game
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from userdata.debriefing import wait_for_debriefing, Debriefing
from userdata.persistency import base_path


class QWaitingForMissionResultWindow(QDialog):

    def __init__(self, gameEvent: Event, game: Game):
        super(QWaitingForMissionResultWindow, self).__init__()
        self.setModal(True)
        self.gameEvent = gameEvent
        self.game = game
        self.setWindowTitle("Waiting for mission completion.")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        self.initUi()
        wait_for_debriefing(lambda debriefing: self.process_debriefing(debriefing))

    def initUi(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("<b>You are clear for takeoff !</b>"))
        self.layout.addWidget(QLabel("In DCS open and play the mission : "))
        self.layout.addWidget(QLabel("<i>liberation_nextturn</i>"))
        self.layout.addWidget(QLabel("or"))
        self.layout.addWidget(QLabel("<i>liberation_nextturn_quick</i>"))
        self.layout.addWidget(QLabel("<b>Then save the debriefing to the folder :</b>"))
        self.layout.addWidget(QLabel(self.debriefing_directory_location()))

        progress = QLabel("")
        progress.setAlignment(QtCore.Qt.AlignCenter)
        progressBar = QMovie("./resources/ui/loader.gif")
        progress.setMovie(progressBar)
        self.layout.addWidget(progress)
        progressBar.start()

        self.setLayout(self.layout)

    def process_debriefing(self, debriefing: Debriefing):

        print("DEBRIEFING !!")

        debriefing.calculate_units(regular_mission=self.gameEvent.operation.regular_mission,
                                   quick_mission=self.gameEvent.operation.quick_mission,
                                   player_country=self.game.player_country,
                                   enemy_country=self.game.enemy_country)

        self.game.finish_event(event=self.gameEvent, debriefing=debriefing)
        self.game.pass_turn(ignored_cps=[self.gameEvent.to_cp, ])

        GameUpdateSignal.get_instance().sendDebriefing(self.game, self.gameEvent, debriefing)
        self.close()

    def debriefing_directory_location(self) -> str:
        return os.path.join(base_path(), "liberation_debriefings")
