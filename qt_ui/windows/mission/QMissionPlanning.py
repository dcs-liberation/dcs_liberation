from PySide2.QtCore import Qt, Slot, QItemSelectionModel, QPoint
from PySide2.QtWidgets import QDialog, QGridLayout, QScrollArea, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox
from game import Game
from game.event import CAP, CAS, FrontlineAttackEvent
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.QWaitingForMissionResultWindow import QWaitingForMissionResultWindow
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView
from qt_ui.windows.mission.QChooseAirbase import QChooseAirbase
from qt_ui.windows.mission.flight.QFlightCreator import QFlightCreator
from qt_ui.windows.mission.flight.QFlightPlanner import QFlightPlanner


class QMissionPlanning(QDialog):

    def __init__(self, game: Game):
        super(QMissionPlanning, self).__init__()
        self.game = game
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(750, 420)
        self.setModal(True)
        self.setWindowTitle("Mission Preparation")
        self.setWindowIcon(EVENT_ICONS["strike"])
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
            self.selected_cp = self.captured_cp[0]

        self.planned_flight_view.selectionModel().setCurrentIndex(self.planned_flight_view.indexAt(QPoint(1, 1)), QItemSelectionModel.Select)
        self.planned_flight_view.selectionModel().selectionChanged.connect(self.on_flight_selection_change)

        if len(self.planned_flight_view.flight_planner.flights) > 0:
            self.flight_planner = QFlightPlanner(self.planned_flight_view.flight_planner.flights[0], self.game)
        else:
            self.flight_planner = QFlightPlanner(None, self.game)

        self.add_flight_button = QPushButton("Add Flight")
        self.add_flight_button.clicked.connect(self.on_add_flight)
        self.delete_flight_button = QPushButton("Delete Selected")
        self.delete_flight_button.clicked.connect(self.on_delete_flight)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.add_flight_button)
        self.button_layout.addWidget(self.delete_flight_button)

        self.mission_start_button = QPushButton("Take Off")
        self.mission_start_button.setProperty("style", "start-button")
        self.mission_start_button.clicked.connect(self.on_start)

        self.left_bar_layout.addWidget(self.select_airbase)
        self.left_bar_layout.addWidget(self.planned_flight_view)
        self.left_bar_layout.addLayout(self.button_layout)

        self.layout.addLayout(self.left_bar_layout, 0, 0)
        self.layout.addWidget(self.flight_planner, 0, 1)
        self.layout.addWidget(self.mission_start_button, 1, 1, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

    @Slot(str)
    def on_departure_cp_changed(self, cp_name):
        cps = [cp for cp in self.game.theater.controlpoints if cp.name == cp_name]
        if len(cps) == 1:
            self.selected_cp = cps[0]
            self.planner = self.game.planners[cps[0].id]
            self.planned_flight_view.set_flight_planner(self.planner)
        else:
            self.planned_flight_view.set_flight_planner(None)

    def on_flight_selection_change(self):
        index = self.planned_flight_view.selectionModel().currentIndex().row()
        flight = self.planner.flights[index]

        self.flight_planner = QFlightPlanner(flight, self.game)
        self.layout.addWidget(self.flight_planner, 0, 1)

    def on_add_flight(self):
        possible_aircraft_type = list(self.selected_cp.base.aircraft.keys())

        if len(possible_aircraft_type) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("No more aircraft are available on " + self.selected_cp.name + " airbase.")
            msg.setWindowTitle("No more aircraft")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
        else:
            self.subwindow = QFlightCreator(self.game, self.selected_cp, possible_aircraft_type, self.planned_flight_view)
            self.subwindow.show()

    def on_delete_flight(self):
        index = self.planned_flight_view.selectionModel().currentIndex().row()
        self.planner.remove_flight(index)
        self.planned_flight_view.set_flight_planner(self.planner)

    def on_start(self):

        for event in self.game.events:
            if isinstance(event, FrontlineAttackEvent) and event.is_player_attacking:
                self.gameEvent = event

        #if self.awacs_checkbox.isChecked() == 1:
        #    self.gameEvent.is_awacs_enabled = True
        #    self.game.awacs_expense_commit()
        #else:
        #    self.gameEvent.is_awacs_enabled = False
        self.gameEvent.is_awacs_enabled = True
        self.gameEvent.ca_slots = 1
        self.gameEvent.departure_cp = self.game.theater.controlpoints[0]
        self.gameEvent.player_attacking({CAS:{}, CAP:{}})
        self.gameEvent.depart_from = self.game.theater.controlpoints[0]

        self.game.initiate_event(self.gameEvent)
        waiting = QWaitingForMissionResultWindow(self.gameEvent, self.game)
        waiting.show()
        self.close()





