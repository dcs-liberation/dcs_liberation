from PySide2 import QtCharts
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QDialog, QGridLayout
from PySide2.QtCharts import QtCharts

import qt_ui.uiconstants as CONST
from game.game import Game


class QStatsWindow(QDialog):

    def __init__(self, game: Game):
        super(QStatsWindow, self).__init__()

        self.game = game

        self.setModal(True)
        self.setWindowTitle("Stats")
        self.setWindowIcon(CONST.ICONS["Statistics"])
        self.setMinimumSize(600, 250)

        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()
        self.generateUnitCharts()
        self.setLayout(self.layout)

    def generateUnitCharts(self):

        self.alliedAircraft = [d.allied_units.aircraft_count for d in self.game.game_stats.data_per_turn]
        self.enemyAircraft = [d.enemy_units.aircraft_count for d in self.game.game_stats.data_per_turn]

        self.alliedAircraftSerie = QtCharts.QLineSeries()
        self.alliedAircraftSerie.setName("Allied aircraft count")
        for a,i in enumerate(self.alliedAircraft):
            self.alliedAircraftSerie.append(QPoint(a, i))

        self.enemyAircraftSerie = QtCharts.QLineSeries()
        self.enemyAircraftSerie.setColor(Qt.red)
        self.enemyAircraftSerie.setName("Enemy aircraft count")
        for a,i in enumerate(self.enemyAircraft):
            self.enemyAircraftSerie.append(QPoint(a, i))

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.alliedAircraftSerie)
        self.chart.addSeries(self.enemyAircraftSerie)
        self.chart.setTitle("Aircraft forces over time")

        self.chart.createDefaultAxes()
        self.chart.axisX().setRange(0, len(self.alliedAircraft))
        self.chart.axisY().setRange(0, max(max(self.alliedAircraft), max(self.enemyAircraft)) + 10)

        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.chartView, 0, 0)

