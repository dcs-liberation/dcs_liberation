import logging
from typing import List, Optional

from PySide2.QtCore import Signal
from PySide2.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from game import Game
from gen.ato import Package
from gen.flights.flight import Flight, FlightType
from gen.flights.flightplan import (
    FlightPlanBuilder,
    PlanningError,
)
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import \
    QFlightWaypointList
from qt_ui.windows.mission.flight.waypoints \
    .QPredefinedWaypointSelectionWindow import \
    QPredefinedWaypointSelectionWindow


class QFlightWaypointTab(QFrame):

    on_flight_changed = Signal()

    def __init__(self, game: Game, package: Package, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.game = game
        self.package = package
        self.flight = flight
        self.planner = FlightPlanBuilder(self.game, package, is_player=True)

        self.flight_waypoint_list: Optional[QFlightWaypointList] = None
        self.ascend_waypoint: Optional[QPushButton] = None
        self.descend_waypoint: Optional[QPushButton] = None
        self.rtb_waypoint: Optional[QPushButton] = None
        self.delete_selected: Optional[QPushButton] = None
        self.open_fast_waypoint_button: Optional[QPushButton] = None
        self.recreate_buttons: List[QPushButton] = []
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.flight_waypoint_list = QFlightWaypointList(self.package,
                                                        self.flight)
        layout.addWidget(self.flight_waypoint_list, 0, 0)

        rlayout = QVBoxLayout()
        layout.addLayout(rlayout, 0, 1)

        rlayout.addWidget(QLabel("<strong>Generator :</strong>"))
        rlayout.addWidget(QLabel("<small>AI compatible</small>"))

        self.recreate_buttons.clear()
        for task in self.package.target.mission_types(for_player=True):
            def make_closure(arg):
                def closure():
                    return self.confirm_recreate(arg)
                return closure
            button = QPushButton(f"Recreate as {task.name}")
            button.clicked.connect(make_closure(task))
            rlayout.addWidget(button)
            self.recreate_buttons.append(button)

        rlayout.addWidget(QLabel("<strong>Advanced : </strong>"))
        rlayout.addWidget(QLabel("<small>Do not use for AI flights</small>"))

        self.ascend_waypoint = QPushButton("Add Ascend Waypoint")
        self.ascend_waypoint.clicked.connect(self.on_ascend_waypoint)
        rlayout.addWidget(self.ascend_waypoint)

        self.descend_waypoint = QPushButton("Add Descend Waypoint")
        self.descend_waypoint.clicked.connect(self.on_descend_waypoint)
        rlayout.addWidget(self.descend_waypoint)

        self.rtb_waypoint = QPushButton("Add RTB Waypoint")
        self.rtb_waypoint.clicked.connect(self.on_rtb_waypoint)
        rlayout.addWidget(self.rtb_waypoint)

        self.delete_selected = QPushButton("Delete Selected")
        self.delete_selected.clicked.connect(self.on_delete_waypoint)
        rlayout.addWidget(self.delete_selected)

        self.open_fast_waypoint_button = QPushButton("Add Waypoint")
        self.open_fast_waypoint_button.clicked.connect(self.on_fast_waypoint)
        rlayout.addWidget(self.open_fast_waypoint_button)
        rlayout.addStretch()
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
        ascend = self.planner.generate_ascend_point(self.flight,
                                                    self.flight.from_cp)
        self.flight.points.append(ascend)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_rtb_waypoint(self):
        rtb = self.planner.generate_rtb_waypoint(self.flight,
                                                 self.flight.from_cp)
        self.flight.points.append(rtb)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_descend_waypoint(self):
        descend = self.planner.generate_descend_point(self.flight,
                                                      self.flight.from_cp)
        self.flight.points.append(descend)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def confirm_recreate(self, task: FlightType) -> None:
        result = QMessageBox.question(
            self,
            "Regenerate flight?",
            ("Changing the flight type will reset its flight plan. Do you want "
             "to continue?"),
            QMessageBox.No,
            QMessageBox.Yes
        )
        original_task = self.flight.flight_type
        if result == QMessageBox.Yes:
            self.flight.flight_type = task
            try:
                self.planner.populate_flight_plan(self.flight)
            except PlanningError as ex:
                self.flight.flight_type = original_task
                logging.exception("Could not recreate flight")
                QMessageBox.critical(
                    self, "Could not recreate flight", str(ex), QMessageBox.Ok
                )
            self.flight_waypoint_list.update_list()
            self.on_change()

    def on_change(self):
        self.flight_waypoint_list.update_list()
        self.on_flight_changed.emit()


