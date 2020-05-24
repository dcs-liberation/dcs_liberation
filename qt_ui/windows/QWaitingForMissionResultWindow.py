import os

from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal
from PySide2.QtGui import QMovie, QIcon
from PySide2.QtWidgets import QLabel, QDialog, QVBoxLayout, QGroupBox, QGridLayout, QPushButton

from game.game import Event, Game
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from userdata.debriefing import wait_for_debriefing, Debriefing
from userdata.persistency import base_path

class DebriefingFileWrittenSignal(QObject):

    instance = None
    debriefingReceived = Signal(Debriefing)

    def __init__(self):
        super(DebriefingFileWrittenSignal, self).__init__()
        DebriefingFileWrittenSignal.instance = self

    def sendDebriefing(self, debriefing: Debriefing):
        self.debriefingReceived.emit(debriefing)

    @staticmethod
    def get_instance():
        return DebriefingFileWrittenSignal.instance

DebriefingFileWrittenSignal()

class QWaitingForMissionResultWindow(QDialog):

    def __init__(self, gameEvent: Event, game: Game):
        super(QWaitingForMissionResultWindow, self).__init__()
        self.setModal(True)
        self.gameEvent = gameEvent
        self.game = game
        self.setWindowTitle("Waiting for mission completion.")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowIcon(QIcon("./resources/icon.png"))

        self.initUi()
        DebriefingFileWrittenSignal.get_instance().debriefingReceived.connect(self.updateLayout)
        wait_for_debriefing(lambda debriefing: self.on_debriefing_udpate(debriefing), self.game)

    def initUi(self):
        self.layout = QGridLayout()
        self.gridLayout = QVBoxLayout()
        self.gridLayout.addWidget(QLabel("<b>You are clear for takeoff</b>"))
        self.gridLayout.addWidget(QLabel(""))
        self.gridLayout.addWidget(QLabel("<h2>For Singleplayer :</h2>"))
        self.gridLayout.addWidget(QLabel("In DCS, open the Mission Editor, and load the file : "))
        self.gridLayout.addWidget(QLabel("<i>liberation_nextturn</i>"))
        self.gridLayout.addWidget(QLabel("Then once the mission is loaded in ME, in menu \"Flight\", click on FLY to launch"))
        self.gridLayout.addWidget(QLabel(""))
        self.gridLayout.addWidget(QLabel("<h2>For Multiplayer</h2>"))
        self.gridLayout.addWidget(QLabel("In DCS, open the Mission Editor, and load the file : "))
        self.gridLayout.addWidget(QLabel("<i>liberation_nextturn</i>"))
        self.gridLayout.addWidget(QLabel("Click on File/Save. Then exit the mission editor, and go to Multiplayer."))
        self.gridLayout.addWidget(QLabel("Then host a server with the mission, and tell your friends to join !"))
        self.gridLayout.addWidget(QLabel("(The step in the mission editor is important, and fix a game breaking bug.)"))
        self.gridLayout.addWidget(QLabel(""))

        progress = QLabel("")
        progress.setAlignment(QtCore.Qt.AlignCenter)
        progressBar = QMovie("./resources/ui/loader.gif")
        progress.setMovie(progressBar)
        self.gridLayout.addWidget(progress)
        self.gridLayout.addWidget(QLabel(""))
        self.gridLayout.addWidget(QLabel("Once you have played the mission, this window will dissapear."))
        self.gridLayout.addWidget(QLabel("You will have to click on \"Accept Results\" to proceed"))

        progressBar.start()
        self.layout.addLayout(self.gridLayout,0,0)
        self.setLayout(self.layout)

    def updateLayout(self, debriefing):
        updateBox = QGroupBox("Mission status")
        updateLayout = QGridLayout()
        updateBox.setLayout(updateLayout)

        updateLayout.addWidget(QLabel("<b>Aircrafts destroyed</b>"), 0, 0)
        updateLayout.addWidget(QLabel(str(len(debriefing.killed_aircrafts))), 0, 1)

        updateLayout.addWidget(QLabel("<b>Ground units destroyed</b>"), 1, 0)
        updateLayout.addWidget(QLabel(str(len(debriefing.killed_ground_units))), 1, 1)

        updateLayout.addWidget(QLabel("<b>Weapons fired</b>"), 2, 0)
        updateLayout.addWidget(QLabel(str(len(debriefing.weapons_fired))), 2, 1)

        updateLayout.addWidget(QLabel("<b>Base Capture Events</b>"), 3, 0)
        updateLayout.addWidget(QLabel(str(len(debriefing.base_capture_events))), 3, 1)

        # Clear previous content of the window
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)

        # Set new window content
        self.gridLayout.addWidget(updateBox, 0, 0)

        if not debriefing.mission_ended:
            self.gridLayout.addWidget(QLabel("<b>Mission is being played</b>"), 1, 0)
        else:
            #self.gridLayout.addWidget(QLabel("<b>Mission is over !</b>"), 1, 0)
            proceed = QPushButton("Accept results")
            proceed.setProperty("style", "btn-primary")
            proceed.clicked.connect(lambda: self.process_debriefing(debriefing))
            self.gridLayout.addWidget(proceed, 1, 0)

    def on_debriefing_udpate(self, debriefing):
        print("On Debriefing update")
        print(debriefing)
        DebriefingFileWrittenSignal.get_instance().sendDebriefing(debriefing)
        wait_for_debriefing(lambda debriefing: self.on_debriefing_udpate(debriefing), self.game)

    def process_debriefing(self, debriefing: Debriefing):
        self.game.finish_event(event=self.gameEvent, debriefing=debriefing)
        self.game.pass_turn(ignored_cps=[self.gameEvent.to_cp, ])

        GameUpdateSignal.get_instance().sendDebriefing(self.game, self.gameEvent, debriefing)
        self.close()

    def debriefing_directory_location(self) -> str:
        return os.path.join(base_path(), "liberation_debriefings")
