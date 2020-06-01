from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton, QSpinBox, \
    QMessageBox
from dcs import Point
from dcs.unittype import UnitType

from game import Game
from gen.flights.ai_flight_planner import FlightPlanner
from gen.flights.flight import Flight, FlightWaypoint, FlightType
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointInfoBox import QFlightWaypointInfoBox
from theater import ControlPoint

PREDEFINED_WAYPOINT_CATEGORIES = [
    "Frontline (CAS AREA)",
    "Building",
    "Units",
    "Airbase"
]


class QFlightCreator(QDialog):

    def __init__(self, game: Game, from_cp:ControlPoint, possible_aircraft_type:List[UnitType], flight_view=None):
        super(QFlightCreator, self).__init__()
        self.game = game
        self.from_cp = from_cp
        self.flight_view = flight_view
        self.planner = self.game.planners[from_cp.id]
        self.available = self.planner.get_available_aircraft()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.setWindowTitle("Create flight")
        self.setWindowIcon(EVENT_ICONS["strike"])

        self.select_type_aircraft = QComboBox()
        for aircraft_type in self.planner.get_available_aircraft().keys():
            print(aircraft_type)
            print(aircraft_type.name)
            self.select_type_aircraft.addItem(aircraft_type.id, userData=aircraft_type)
        self.select_type_aircraft.setCurrentIndex(0)

        self.select_flight_type = QComboBox()
        self.select_flight_type.addItem("CAP [Combat Air Patrol]", userData=FlightType.CAP)
        self.select_flight_type.addItem("BARCAP [Barrier Combat Air Patrol]", userData=FlightType.BARCAP)
        self.select_flight_type.addItem("TARCAP [Target Combat Air Patrol]", userData=FlightType.TARCAP)
        self.select_flight_type.addItem("INTERCEPT [Interception]", userData=FlightType.INTERCEPTION)
        self.select_flight_type.addItem("CAS [Close Air Support]", userData=FlightType.CAS)
        self.select_flight_type.addItem("BAI [Battlefield Interdiction]", userData=FlightType.BAI)
        self.select_flight_type.addItem("SEAD [Suppression of Enemy Air Defenses]", userData=FlightType.SEAD)
        self.select_flight_type.addItem("DEAD [Destruction of Enemy Air Defenses]", userData=FlightType.DEAD)
        self.select_flight_type.addItem("STRIKE [Strike]", userData=FlightType.STRIKE)
        self.select_flight_type.addItem("ANTISHIP [Antiship Attack]", userData=FlightType.ANTISHIP)
        self.select_flight_type.setCurrentIndex(0)

        self.select_count_of_aircraft = QSpinBox()
        self.select_count_of_aircraft.setMinimum(1)
        self.select_count_of_aircraft.setMaximum(4)
        self.select_count_of_aircraft.setValue(2)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.create_flight)

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout()

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type of Aircraft : "))
        type_layout.addStretch()
        type_layout.addWidget(self.select_type_aircraft, alignment=Qt.AlignRight)

        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Count : "))
        count_layout.addStretch()
        count_layout.addWidget(self.select_count_of_aircraft, alignment=Qt.AlignRight)

        flight_type_layout = QHBoxLayout()
        flight_type_layout.addWidget(QLabel("Task : "))
        flight_type_layout.addStretch()
        flight_type_layout.addWidget(self.select_flight_type, alignment=Qt.AlignRight)

        layout.addLayout(type_layout)
        layout.addLayout(count_layout)
        layout.addLayout(flight_type_layout)
        layout.addStretch()
        layout.addWidget(self.add_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def create_flight(self):
        aircraft_type = self.select_type_aircraft.currentData()
        count = self.select_count_of_aircraft.value()

        if self.available[aircraft_type] < count:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Not enough aircraft of this type are available. Only " + str(self.available[aircraft_type]) + " available.")
            msg.setWindowTitle("Not enough aircraft")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec_()
            return
        else:
            flight = Flight(aircraft_type, count, self.from_cp, self.select_flight_type.currentData())
            self.planner.flights.append(flight)
            self.planner.custom_flights.append(flight)
            if self.flight_view is not None:
                self.flight_view.set_flight_planner(self.planner, len(self.planner.flights)-1)
            self.close()

