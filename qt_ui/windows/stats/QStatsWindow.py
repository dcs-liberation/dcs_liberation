from PySide2.QtWidgets import QDialog, QGridLayout, QTabWidget

import qt_ui.uiconstants as CONST
from game.game import Game
from qt_ui.windows.stats.QAircraftChart import QAircraftChart
from qt_ui.windows.stats.QArmorChart import QArmorChart


class QStatsWindow(QDialog):
    def __init__(self, game: Game):
        super(QStatsWindow, self).__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Stats")
        self.setWindowIcon(CONST.ICONS["Statistics"])
        self.setMinimumSize(600, 300)

        self.layout = QGridLayout()
        self.aircraft_charts = QAircraftChart(self.game)
        self.armor_charts = QArmorChart(self.game)
        self.tabview = QTabWidget()
        self.tabview.addTab(self.aircraft_charts, "Aircraft")
        self.tabview.addTab(self.armor_charts, "Armor")
        self.layout.addWidget(self.tabview, 0, 0)
        self.setLayout(self.layout)
