from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QLabel, QDialog, QVBoxLayout, QGroupBox, QGridLayout, QPushButton

from game.game import Event, db, Game
from userdata.debriefing import Debriefing


class QDebriefingWindow(QDialog):

    def __init__(self, debriefing: Debriefing, gameEvent: Event, game: Game):
        super(QDebriefingWindow, self).__init__()

        self.setModal(True)
        self.setWindowTitle("Debriefing")
        self.setMinimumSize(300, 200)
        self.setWindowIcon(QIcon("./resources/icon.png"))

        self.game = game
        self.gameEvent = gameEvent
        self.debriefing = debriefing

        self.player_losses = debriefing.destroyed_units.get(self.game.player_country, {})
        self.enemy_losses = debriefing.destroyed_units.get(self.game.enemy_country, {})

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout()

        # Result

        if self.gameEvent.is_successfull(self.debriefing):
            title = QLabel("<b>Operation Succesfull !</b>")
            title.setProperty("style", "title-success")
        else:
            title = QLabel("<b>Operation failed !</b>")
            title.setProperty("style", "title-danger")
        self.layout.addWidget(title)

        # Player lost units
        lostUnits = QGroupBox(self.game.player_country + "'s lost units :")
        lostUnitsLayout = QGridLayout()
        lostUnits.setLayout(lostUnitsLayout)

        row = 0
        for unit_type, count in self.player_losses.items():
            lostUnitsLayout.addWidget(QLabel(db.unit_type_name(unit_type)), row, 0)
            lostUnitsLayout.addWidget(QLabel("{}".format(count)), row, 1)
            row += 1

        self.layout.addWidget(lostUnits)

        # Enemy lost units
        enemylostUnits = QGroupBox(self.game.enemy_country + "'s lost units :")
        enemylostUnitsLayout = QGridLayout()
        enemylostUnits.setLayout(enemylostUnitsLayout)

        row = 0
        if self.debriefing.destroyed_objects:
            enemylostUnitsLayout.addWidget(QLabel("Ground assets"), row, 0)
            enemylostUnitsLayout.addWidget(QLabel("{}".format(len(self.debriefing.destroyed_objects))), row, 1)
            row += 1

        for unit_type, count in self.enemy_losses.items():
            if count == 0:
                continue
            enemylostUnitsLayout.addWidget(QLabel(db.unit_type_name(unit_type)), row, 0)
            enemylostUnitsLayout.addWidget(QLabel("{}".format(count)), row, 1)
            row += 1

        self.layout.addWidget(enemylostUnits)

        # confirm button
        okay = QPushButton("Okay")
        okay.clicked.connect(self.close)
        self.layout.addWidget(okay)

        self.setLayout(self.layout)
