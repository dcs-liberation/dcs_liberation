from typing import Iterable, List, Optional

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
from gen.flights.flight import Flight, FlightType, FlightWaypoint
from gen.flights.flightplan import (
    CustomFlightPlan,
    FlightPlanBuilder,
    StrikeFlightPlan,
)
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import \
    QFlightWaypointList
from qt_ui.windows.mission.flight.waypoints \
    .QPredefinedWaypointSelectionWindow import \
    QPredefinedWaypointSelectionWindow
from theater import FrontLine


class QFlightWaypointTab(QFrame):

    on_flight_changed = Signal()

    def __init__(self, game: Game, package: Package, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.game = game
        self.package = package
        self.flight = flight
        self.planner = FlightPlanBuilder(self.game, package, is_player=True)

        self.flight_waypoint_list: Optional[QFlightWaypointList] = None
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

        # TODO: Filter by objective type.
        self.recreate_buttons.clear()
        recreate_types = [
            FlightType.CAS,
            FlightType.CAP,
            FlightType.DEAD,
            FlightType.ESCORT,
            FlightType.SEAD,
            FlightType.STRIKE
        ]
        for task in recreate_types:
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
            self.delete_waypoint(self.flight.flight_plan.waypoints[wpt])
            self.flight_waypoint_list.update_list()
        self.on_change()

    def delete_waypoint(self, waypoint: FlightWaypoint) -> None:
        # Need to degrade to a custom flight plan and remove the waypoint.
        # If the waypoint is a target waypoint and is not the last target
        # waypoint, we don't need to degrade.
        if isinstance(self.flight.flight_plan, StrikeFlightPlan):
            is_target = waypoint in self.flight.flight_plan.targets
            if is_target and len(self.flight.flight_plan.targets) > 1:
                self.flight.flight_plan.targets.remove(waypoint)
                return

        self.degrade_to_custom_flight_plan()
        self.flight.flight_plan.waypoints.remove(waypoint)

    def on_fast_waypoint(self):
        self.subwindow = QPredefinedWaypointSelectionWindow(self.game, self.flight, self.flight_waypoint_list)
        self.subwindow.waypoints_added.connect(self.on_waypoints_added)
        self.subwindow.show()

    def on_waypoints_added(self, waypoints: Iterable[FlightWaypoint]) -> None:
        if not waypoints:
            return
        self.degrade_to_custom_flight_plan()
        self.flight.flight_plan.waypoints.extend(waypoints)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_rtb_waypoint(self):
        rtb = self.planner.generate_rtb_waypoint(self.flight,
                                                 self.flight.from_cp)
        self.degrade_to_custom_flight_plan()
        self.flight.flight_plan.waypoints.append(rtb)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def degrade_to_custom_flight_plan(self) -> None:
        if not isinstance(self.flight.flight_plan, CustomFlightPlan):
            self.flight.flight_plan = CustomFlightPlan(
                package=self.flight.package,
                flight=self.flight,
                custom_waypoints=self.flight.flight_plan.waypoints
            )

    def confirm_recreate(self, task: FlightType) -> None:
        result = QMessageBox.question(
            self,
            "Regenerate flight?",
            ("Changing the flight type will reset its flight plan. Do you want "
             "to continue?"),
            QMessageBox.No,
            QMessageBox.Yes
        )
        if result == QMessageBox.Yes:
            # TODO: Should be buttons for both BARCAP and TARCAP.
            # BARCAP and TARCAP behave differently. TARCAP arrives a few minutes
            # ahead of the rest of the package and stays until the package
            # departs, whereas BARCAP usually isn't part of a strike package and
            # has a fixed mission time.
            if task == FlightType.CAP:
                if isinstance(self.package.target, FrontLine):
                    task = FlightType.TARCAP
                else:
                    task = FlightType.BARCAP
            self.flight.flight_type = task
            self.planner.populate_flight_plan(self.flight)
            self.flight_waypoint_list.update_list()
            self.on_change()

    def on_change(self):
        self.flight_waypoint_list.update_list()
        self.on_flight_changed.emit()


