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

from game import db
from game.debriefing import Debriefing


class QDebriefingWindow(QDialog):
    def __init__(self, debriefing: Debriefing):
        super(QDebriefingWindow, self).__init__()
        self.debriefing = debriefing

        self.setModal(True)
        self.setWindowTitle("Debriefing")
        self.setMinimumSize(300, 200)
        self.setWindowIcon(QIcon("./resources/icon.png"))

        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap("./resources/ui/debriefing.png")
        header.setPixmap(pixmap)
        self.layout.addWidget(header)
        self.layout.addStretch()

        title = QLabel("<b>Casualty report</b>")
        self.layout.addWidget(title)

        # Player lost units
        lostUnits = QGroupBox(f"{self.debriefing.player_country}'s lost units:")
        lostUnitsLayout = QGridLayout()
        lostUnits.setLayout(lostUnitsLayout)

        row = 0
        player_air_losses = self.debriefing.air_losses.by_type(player=True)
        for unit_type, count in player_air_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(
                        db.unit_get_expanded_info(
                            self.debriefing.player_country, unit_type, "name"
                        )
                    ),
                    row,
                    0,
                )
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        front_line_losses = self.debriefing.front_line_losses_by_type(player=True)
        for unit_type, count in front_line_losses.items():
            try:
                lostUnitsLayout.addWidget(QLabel(db.unit_type_name(unit_type)), row, 0)
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        convoy_losses = self.debriefing.convoy_losses_by_type(player=True)
        for unit_type, count in convoy_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(f"{db.unit_type_name(unit_type)} from convoy"), row, 0
                )
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        airlift_losses = self.debriefing.airlift_losses_by_type(player=True)
        for unit_type, count in airlift_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(f"{db.unit_type_name(unit_type)} from airlift"), row, 0
                )
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        building_losses = self.debriefing.building_losses_by_type(player=True)
        for building, count in building_losses.items():
            try:
                lostUnitsLayout.addWidget(QLabel(building), row, 0)
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {building} to debriefing information")

        self.layout.addWidget(lostUnits)

        # Enemy lost units
        enemylostUnits = QGroupBox(f"{self.debriefing.enemy_country}'s lost units:")
        enemylostUnitsLayout = QGridLayout()
        enemylostUnits.setLayout(enemylostUnitsLayout)

        enemy_air_losses = self.debriefing.air_losses.by_type(player=False)
        for unit_type, count in enemy_air_losses.items():
            try:
                enemylostUnitsLayout.addWidget(
                    QLabel(
                        db.unit_get_expanded_info(
                            self.debriefing.enemy_country, unit_type, "name"
                        )
                    ),
                    row,
                    0,
                )
                enemylostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        front_line_losses = self.debriefing.front_line_losses_by_type(player=False)
        for unit_type, count in front_line_losses.items():
            if count == 0:
                continue
            enemylostUnitsLayout.addWidget(QLabel(db.unit_type_name(unit_type)), row, 0)
            enemylostUnitsLayout.addWidget(QLabel("{}".format(count)), row, 1)
            row += 1

        convoy_losses = self.debriefing.convoy_losses_by_type(player=False)
        for unit_type, count in convoy_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(f"{db.unit_type_name(unit_type)} from convoy"), row, 0
                )
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        airlift_losses = self.debriefing.airlift_losses_by_type(player=False)
        for unit_type, count in airlift_losses.items():
            try:
                lostUnitsLayout.addWidget(
                    QLabel(f"{db.unit_type_name(unit_type)} from airlift"), row, 0
                )
                lostUnitsLayout.addWidget(QLabel(str(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {unit_type} to debriefing information")

        building_losses = self.debriefing.building_losses_by_type(player=False)
        for building, count in building_losses.items():
            try:
                enemylostUnitsLayout.addWidget(QLabel(building), row, 0)
                enemylostUnitsLayout.addWidget(QLabel("{}".format(count)), row, 1)
                row += 1
            except AttributeError:
                logging.exception(f"Issue adding {building} to debriefing information")

        self.layout.addWidget(enemylostUnits)

        # TODO: Display dead ground object units and runways.

        # confirm button
        okay = QPushButton("Okay")
        okay.clicked.connect(self.close)
        self.layout.addWidget(okay)

        self.setLayout(self.layout)
