from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QPoint, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QFrame, QGridLayout
from game import Game


class QAircraftChart(QFrame):
    def __init__(self, game: Game):
        super(QAircraftChart, self).__init__()
        self.game = game
        self.initUi()

    def initUi(self):
        self.layout = QGridLayout()
        self.generateUnitCharts()
        self.setLayout(self.layout)

    def generateUnitCharts(self):

        self.alliedAircraft = [
            d.allied_units.aircraft_count for d in self.game.game_stats.data_per_turn
        ]
        self.enemyAircraft = [
            d.enemy_units.aircraft_count for d in self.game.game_stats.data_per_turn
        ]

        self.alliedAircraftSerie = QtCharts.QLineSeries()
        self.alliedAircraftSerie.setName("Allied aircraft count")
        for a, i in enumerate(self.alliedAircraft):
            self.alliedAircraftSerie.append(QPoint(a, i))

        self.enemyAircraftSerie = QtCharts.QLineSeries()
        self.enemyAircraftSerie.setColor(Qt.red)
        self.enemyAircraftSerie.setName("Enemy aircraft count")
        for a, i in enumerate(self.enemyAircraft):
            self.enemyAircraftSerie.append(QPoint(a, i))

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.alliedAircraftSerie)
        self.chart.addSeries(self.enemyAircraftSerie)
        self.chart.setTitle("Aircraft forces over time")

        self.chart.createDefaultAxes()
        self.chart.axisX().setTitleText("Turn")
        self.chart.axisX().setLabelFormat("%i")
        self.chart.axisX().setRange(0, len(self.alliedAircraft))
        self.chart.axisX().applyNiceNumbers()

        self.chart.axisY().setLabelFormat("%i")
        self.chart.axisY().setRange(
            0, max(max(self.alliedAircraft), max(self.enemyAircraft)) + 10
        )
        self.chart.axisY().applyNiceNumbers()

        self.chartView = QtCharts.QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.layout.addWidget(self.chartView, 0, 0)
