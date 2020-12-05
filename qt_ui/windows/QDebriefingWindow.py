import logging

from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (
    QDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from game.debriefing import Debriefing
from game.game import Event, Game, db


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

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap("./resources/ui/debriefing.png")
        header.setPixmap(pixmap)
        self.layout.addWidget(header)
        self.layout.addStretch()

        # Result
        #if self.gameEvent.is_successfull(self.debriefing):
        #    title = QLabel("<b>Operation end !</b>")
        #    title.setProperty("style", "title-success")
        #else:
        #    title = QLabel("<b>Operation end !</b>")
        #    title.setProperty("style", "title-danger")
        title = QLabel("<b>Casualty report</b>")
        self.layout.addWidget(title)

        # Player lost units
        lostUnits = QGroupBox(self.game.player_country + "'s lost units :")
        lostUnitsLayout = QGridLayout()
        lostUnits.setLayout(lostUnitsLayout)

        row = 0
        player_air_losses = self.debriefing.air_losses.by_type(player=True)
        for unit_type, count in player_air_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(db.unit_type_name(unit_type)), row, 0)
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(
                    f"Issue adding {unit_type} to debriefing information")

        front_line_losses = self.debriefing.front_line_losses.by_type(
            player=True
        )
        for unit_type, count in front_line_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(db.unit_type_name(unit_type)), row, 0)
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(
                    f"Issue adding {unit_type} to debriefing information")

        for building, count in self.debriefing.player_dead_buildings_dict.items():
            try:
                lostUnitsLayout.addWidget(QLabel(building, row, 0))
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(
                    f"Issue adding {building} to debriefing information")

        self.layout.addWidget(lostUnits)

        # Enemy lost units
        enemylostUnits = QGroupBox(self.game.enemy_country + "'s lost units :")
        enemylostUnitsLayout = QGridLayout()
        enemylostUnits.setLayout(enemylostUnitsLayout)

        #row = 0
        #if self.debriefing.destroyed_objects:
        #    enemylostUnitsLayout.addWidget(QLabel("Ground assets"), row, 0)
        #    enemylostUnitsLayout.addWidget(QLabel("{}".format(len(self.debriefing.destroyed_objects))), row, 1)
        #    row += 1

        enemy_air_losses = self.debriefing.air_losses.by_type(player=False)
        for unit_type, count in enemy_air_losses.items():
            try:
                enemylostUnitsLayout.addWidget(
                    QLabel(db.unit_type_name(unit_type)), row, 0)
                enemylostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(
                    f"Issue adding {unit_type} to debriefing information")

        front_line_losses = self.debriefing.front_line_losses.by_type(
            player=False
        )
        for unit_type, count in front_line_losses.items():
            if count == 0:
                continue
            enemylostUnitsLayout.addWidget(QLabel(db.unit_type_name(unit_type)), row, 0)
            enemylostUnitsLayout.addWidget(QLabel("{}".format(count)), row, 1)
            row += 1

        for building, count in self.debriefing.enemy_dead_buildings_dict.items():
            try:
                enemylostUnitsLayout.addWidget(QLabel(building), row, 0)
                enemylostUnitsLayout.addWidget(QLabel("{}".format(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(
                    f"Issue adding {building} to debriefing information")

        self.layout.addWidget(enemylostUnits)

        # confirm button
        okay = QPushButton("Okay")
        okay.clicked.connect(self.close)
        self.layout.addWidget(okay)

        self.setLayout(self.layout)
