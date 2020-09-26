from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout

from game import Game
from gen.flights.flight import Flight
from gen.flights.flightplan import FlightPlanBuilder
from qt_ui.windows.mission.flight.generator.QCAPMissionGenerator import QCAPMissionGenerator
from qt_ui.windows.mission.flight.generator.QCASMissionGenerator import QCASMissionGenerator
from qt_ui.windows.mission.flight.generator.QSEADMissionGenerator import QSEADMissionGenerator
from qt_ui.windows.mission.flight.generator.QSTRIKEMissionGenerator import QSTRIKEMissionGenerator
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import QFlightWaypointList
from qt_ui.windows.mission.flight.waypoints.QPredefinedWaypointSelectionWindow import QPredefinedWaypointSelectionWindow


class QFlightWaypointTab(QFrame):

    on_flight_changed = Signal()

    def __init__(self, game: Game, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.flight = flight
        self.game = game
        self.planner = FlightPlanBuilder(self.game, is_player=True)
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        rlayout = QVBoxLayout()
        self.flight_waypoint_list = QFlightWaypointList(self.flight)
        self.open_fast_waypoint_button = QPushButton("Add Waypoint")
        self.open_fast_waypoint_button.clicked.connect(self.on_fast_waypoint)

        self.cas_generator = QPushButton("Gen. CAS")
        self.cas_generator.clicked.connect(self.on_cas_generator)

        self.cap_generator = QPushButton("Gen. CAP")
        self.cap_generator.clicked.connect(self.on_cap_generator)

        self.sead_generator = QPushButton("Gen. SEAD/DEAD")
        self.sead_generator.clicked.connect(self.on_sead_generator)

        self.strike_generator = QPushButton("Gen. STRIKE")
        self.strike_generator.clicked.connect(self.on_strike_generator)

        self.rtb_waypoint = QPushButton("Add RTB Waypoint")
        self.rtb_waypoint.clicked.connect(self.on_rtb_waypoint)

        self.ascend_waypoint = QPushButton("Add Ascend Waypoint")
        self.ascend_waypoint.clicked.connect(self.on_ascend_waypoint)

        self.descend_waypoint = QPushButton("Add Descend Waypoint")
        self.descend_waypoint.clicked.connect(self.on_descend_waypoint)

        self.delete_selected = QPushButton("Delete Selected")
        self.delete_selected.clicked.connect(self.on_delete_waypoint)

        layout.addWidget(self.flight_waypoint_list, 0, 0)

        rlayout.addWidget(QLabel("<strong>Generator :</strong>"))
        rlayout.addWidget(QLabel("<small>AI compatible</small>"))
        rlayout.addWidget(self.cas_generator)
        rlayout.addWidget(self.cap_generator)
        rlayout.addWidget(self.sead_generator)
        rlayout.addWidget(self.strike_generator)
        rlayout.addWidget(QLabel("<strong>Advanced : </strong>"))
        rlayout.addWidget(QLabel("<small>Do not use for AI flights</small>"))
        rlayout.addWidget(self.ascend_waypoint)
        rlayout.addWidget(self.descend_waypoint)
        rlayout.addWidget(self.rtb_waypoint)
        rlayout.addWidget(self.open_fast_waypoint_button)
        rlayout.addWidget(self.delete_selected)
        rlayout.addStretch()
        layout.addLayout(rlayout, 0, 1)
        self.setLayout(layout)

    def on_delete_waypoint(self):
        wpt = self.flight_waypoint_list.selectionModel().currentIndex().row()
        if wpt > 0:
            del self.flight.points[wpt-1]
            self.flight_waypoint_list.update_list()
        self.on_change()

    def on_fast_waypoint(self):
        self.subwindow = QPredefinedWaypointSelectionWindow(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.finished.connect(self.on_change)
        self.subwindow.show()

    def on_ascend_waypoint(self):
        ascend = self.planner.generate_ascend_point(self.flight.from_cp)
        self.flight.points.append(ascend)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_rtb_waypoint(self):
        rtb = self.planner.generate_rtb_waypoint(self.flight.from_cp)
        self.flight.points.append(rtb)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_descend_waypoint(self):
        descend = self.planner.generate_descend_point(self.flight.from_cp)
        self.flight.points.append(descend)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_cas_generator(self):
        self.subwindow = QCASMissionGenerator(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.finished.connect(self.on_change)
        self.subwindow.show()

    def on_cap_generator(self):
        self.subwindow = QCAPMissionGenerator(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.finished.connect(self.on_change)
        self.subwindow.show()

    def on_sead_generator(self):
        self.subwindow = QSEADMissionGenerator(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.finished.connect(self.on_change)
        self.subwindow.show()

    def on_strike_generator(self):
        self.subwindow = QSTRIKEMissionGenerator(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.finished.connect(self.on_change)
        self.subwindow.show()

    def on_change(self):
        self.flight_waypoint_list.update_list()
        self.on_flight_changed.emit()


