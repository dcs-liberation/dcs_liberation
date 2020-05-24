from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton
from dcs import Point

from game import Game
from gen.flights.flight import Flight, FlightWaypoint
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointInfoBox import QFlightWaypointInfoBox

PREDEFINED_WAYPOINT_CATEGORIES = [
    "Frontline (CAS AREA)",
    "Building",
    "Units",
    "Airbase"
]


class QWaypointSelectionWindow(QDialog):


    def __init__(self, game: Game, flight: Flight, flight_waypoint_list):
        super(QWaypointSelectionWindow, self).__init__()
        self.game = game
        self.flight = flight
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(450, 350)
        self.setModal(True)
        self.setWindowTitle("Add Predefined Waypoint")
        self.setWindowIcon(EVENT_ICONS["strike"])
        self.flight_waypoint_list = flight_waypoint_list

        self.selected_cp = self.game.theater.controlpoints[0]
        self.cp_selection_box = QComboBox()
        for cp in self.game.theater.controlpoints:
            self.cp_selection_box.addItem(cp.name)

        self.wpt_type_selection_box = QComboBox()
        for cat in PREDEFINED_WAYPOINT_CATEGORIES:
            self.wpt_type_selection_box.addItem(cat)

        self.cp_selection_box.currentTextChanged.connect(self.on_parameters_changed)
        self.wpt_type_selection_box.currentTextChanged.connect(self.on_parameters_changed)

        self.wpt_selection_box = QComboBox()
        self.wpt_selection_box.setMinimumWidth(200)
        self.wpt_selection_box.currentTextChanged.connect(self.on_select_wpt_changed)

        self.selected_waypoint = None
        self.wpt_info = QFlightWaypointInfoBox(self.selected_waypoint)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_waypoint)

        self.init_ui()
        self.on_parameters_changed()
        print("DONE")


    def init_ui(self):
        layout = QVBoxLayout()

        near_layout = QHBoxLayout()
        near_layout.addWidget(QLabel("Near : "))
        near_layout.addWidget(self.cp_selection_box)
        near_layout.addStretch()

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type : "))
        type_layout.addWidget(self.wpt_type_selection_box)
        type_layout.addStretch()

        wpt_layout = QHBoxLayout()
        wpt_layout.addWidget(QLabel("Waypoint : "))
        wpt_layout.addWidget(self.wpt_selection_box)
        wpt_layout.addStretch()

        layout.addLayout(near_layout)
        layout.addLayout(type_layout)
        layout.addLayout(wpt_layout)
        layout.addWidget(self.wpt_info)
        layout.addStretch()
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def on_select_wpt_changed(self):
        self.selected_waypoint = self.wpt_selection_box.currentData()
        self.wpt_info.set_flight_waypoint(self.selected_waypoint)
        if self.selected_waypoint is None:
            self.add_button.setDisabled(True)
        else:
            self.add_button.setDisabled(False)

    def on_parameters_changed(self):
        self.wpt_selection_box.clear()

        select_cp_text = self.cp_selection_box.currentText()
        select_cp = None
        for cp in self.game.theater.controlpoints:
            if cp.name == select_cp_text:
                select_cp = cp
                break
        if select_cp is not None:
            selected_wpt_type = self.wpt_type_selection_box.currentText()

            if selected_wpt_type == PREDEFINED_WAYPOINT_CATEGORIES[0]: # CAS
                enemy_cp = [cp for cp in select_cp.connected_points if cp.captured != select_cp.captured]
                for ecp in enemy_cp:
                    wpt = FlightWaypoint((select_cp.position.x + ecp.position.x)/2, (select_cp.position.y + ecp.position.y)/2, 800)
                    wpt.name = "Frontline with " + ecp.name + " [CAS]"
                    wpt.description = "Provide CAS"
                    self.wpt_selection_box.addItem(wpt.name, userData=wpt)
                if len(enemy_cp) == 0:
                    self.wpt_selection_box.addItem("None", userData=None)
            elif selected_wpt_type == PREDEFINED_WAYPOINT_CATEGORIES[1]:  # Building
                for ground_object in select_cp.ground_objects:
                    if not ground_object.is_dead and not ground_object.dcs_identifier == "AA":
                        wpt = FlightWaypoint(ground_object.position.x,ground_object.position.y, 0)
                        wpt.name = ground_object.category + " #" + str(ground_object.object_id) + " @ site #" + str(ground_object.group_id)
                        wpt.description = "Ennemy Building"
                        self.wpt_selection_box.addItem(wpt.name, userData=wpt)
            elif selected_wpt_type == PREDEFINED_WAYPOINT_CATEGORIES[2]:  # Known units position
                for ground_object in select_cp.ground_objects:
                    if not ground_object.is_dead and ground_object.dcs_identifier == "AA":
                        for g in ground_object.groups:
                            for u in g.units:
                                wpt = FlightWaypoint(ground_object.position.x, ground_object.position.y, 0)
                                wpt.name = u.type + " @ site #" + str(ground_object.group_id)
                                wpt.description = "Ennemy unit to be destroyed"
                                self.wpt_selection_box.addItem(wpt.name, userData=wpt)
            elif selected_wpt_type == PREDEFINED_WAYPOINT_CATEGORIES[3]:  # CAS
                wpt = FlightWaypoint(select_cp.position.x, select_cp.position.y, 0)
                wpt.name = select_cp.name
                wpt.description = "Position of " + select_cp.name
                self.wpt_selection_box.addItem("Airbase", userData=wpt)
            else:
                self.wpt_selection_box.addItem("None", userData=None)
        else:
            self.wpt_selection_box.addItem("None", userData=None)

        self.wpt_selection_box.setCurrentIndex(0)

    def add_waypoint(self):
        if not self.selected_waypoint is None:
            self.flight.points.append(self.selected_waypoint)
        self.flight_waypoint_list.update_list()
        self.close()



