from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QFrame, QGridLayout
from game import Game


class QArmorChart(QFrame):
    def __init__(self, game: Game):
        super(QArmorChart, self).__init__()
        self.game = game
        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()
        self.generateUnitCharts()
        self.setLayout(self.layout)

    def generateUnitCharts(self):

        self.alliedArmor = [
            d.allied_units.vehicles_count for d in self.game.game_stats.data_per_turn
        ]
        self.enemyArmor = [
            d.enemy_units.vehicles_count for d in self.game.game_stats.data_per_turn
        ]

        self.alliedArmorSerie = QtCharts.QLineSeries()
        self.alliedArmorSerie.setName("Allied vehicle count")
        for a, i in enumerate(self.alliedArmor):
            self.alliedArmorSerie.append(QPoint(a, i))

        self.enemyArmorSerie = QtCharts.QLineSeries()
        self.enemyArmorSerie.setColor(Qt.red)
        self.enemyArmorSerie.setName("Enemy vehicle count")
        for a, i in enumerate(self.enemyArmor):
            self.enemyArmorSerie.append(QPoint(a, i))

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.alliedArmorSerie)
        self.chart.addSeries(self.enemyArmorSerie)
        self.chart.setTitle("Combat vehicles over time")

        self.chart.createDefaultAxes()
        self.chart.axisX().setTitleText("Turn")
        self.chart.axisX().setLabelFormat("%i")
        self.chart.axisX().setRange(0, len(self.alliedArmor))
        self.chart.axisX().applyNiceNumbers()

        self.chart.axisY().setLabelFormat("%i")
        self.chart.axisY().setRange(
            0, max(max(self.alliedArmor), max(self.enemyArmor)) + 10
        )
        self.chart.axisY().applyNiceNumbers()

        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.chartView, 0, 0)
