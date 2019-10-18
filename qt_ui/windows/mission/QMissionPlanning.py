from PySide2.QtCore import Qt, Slot, QItemSelectionModel, QPoint
from PySide2.QtWidgets import QDialog, QGridLayout, QScrollArea, QVBoxLayout
from game import Game
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView
from qt_ui.windows.mission.QChooseAirbase import QChooseAirbase
from qt_ui.windows.mission.flight.QFlightPlanner import QFlightPlanner


class QMissionPlanning(QDialog):

    def __init__(self, game: Game):
        super(QMissionPlanning, self).__init__()
        self.game = game
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(750, 350)
        self.setModal(True)
        self.setWindowTitle("Mission Preparation")
        self.init_ui()
        print("DONE")

    def init_ui(self):

        self.captured_cp = [cp for cp in self.game.theater.controlpoints if cp.captured]

        self.layout = QGridLayout()
        self.left_bar_layout = QVBoxLayout()

        self.select_airbase = QChooseAirbase(self.game)
        self.select_airbase.selected_airbase_changed.connect(self.on_departure_cp_changed)
        self.planned_flight_view = QPlannedFlightsView(None)
        if self.captured_cp[0].id in self.game.planners.keys():
            self.planner = self.game.planners[self.captured_cp[0].id]
            self.planned_flight_view.set_flight_planner(self.planner)

        self.planned_flight_view.selectionModel().setCurrentIndex(self.planned_flight_view.indexAt(QPoint(1, 1)), QItemSelectionModel.Select)
        self.planned_flight_view.selectionModel().selectionChanged.connect(self.on_flight_selection_change)

        self.flight_planner = QFlightPlanner(self.planned_flight_view.flight_planner.flights[0], self.game)


        self.left_bar_layout.addWidget(self.select_airbase)
        self.left_bar_layout.addWidget(self.planned_flight_view)

        self.layout.addLayout(self.left_bar_layout, 0, 0)
        self.layout.addWidget(self.flight_planner, 0, 1)

        self.setLayout(self.layout)

    @Slot(str)
    def on_departure_cp_changed(self, cp_name):
        cps = [cp for cp in self.game.theater.controlpoints if cp.name == cp_name]
        if len(cps) == 1:
            self.planner = self.game.planners[cps[0].id]
            self.planned_flight_view.set_flight_planner(self.planner)
        else:
            self.planned_flight_view.set_flight_planner(None)

    def on_flight_selection_change(self):
        index = self.planned_flight_view.selectionModel().currentIndex().row()
        flight = self.planner.flights[index]

        self.flight_planner = QFlightPlanner(flight, self.game)
        self.layout.addWidget(self.flight_planner,0 ,1)
