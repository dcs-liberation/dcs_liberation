import logging
from typing import Iterable, List, Optional, Any

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
from game.ato.flight import Flight
from game.ato.flightplans.custom import CustomFlightPlan, CustomLayout
from game.ato.flightplans.flightplan import FlightPlan
from game.ato.flightplans.flightplanbuilder import FlightPlanBuilder
from game.ato.flightplans.formationattack import FormationAttackFlightPlan
from game.ato.flightplans.planningerror import PlanningError
from game.ato.flighttype import FlightType
from game.ato.flightwaypoint import FlightWaypoint
from game.ato.loadouts import Loadout
from game.ato.package import Package
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointList import (
    QFlightWaypointList,
)
from qt_ui.windows.mission.flight.waypoints.QPredefinedWaypointSelectionWindow import (
    QPredefinedWaypointSelectionWindow,
)


class QFlightWaypointTab(QFrame):
    loadout_changed = Signal()

    def __init__(self, game: Game, package: Package, flight: Flight):
        super(QFlightWaypointTab, self).__init__()
        self.game = game
        self.package = package
        self.flight = flight
        self.planner = FlightPlanBuilder(package, game.blue, game.theater)

        self.flight_waypoint_list: Optional[QFlightWaypointList] = None
        self.rtb_waypoint: Optional[QPushButton] = None
        self.delete_selected: Optional[QPushButton] = None
        self.open_fast_waypoint_button: Optional[QPushButton] = None
        self.recreate_buttons: List[QPushButton] = []
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        self.flight_waypoint_list = QFlightWaypointList(self.package, self.flight)
        layout.addWidget(self.flight_waypoint_list, 0, 0)

        rlayout = QVBoxLayout()
        layout.addLayout(rlayout, 0, 1)

        rlayout.addWidget(QLabel("<strong>Generator :</strong>"))
        rlayout.addWidget(QLabel("<small>AI compatible</small>"))

        self.recreate_buttons.clear()
        for task in self.package.target.mission_types(for_player=True):

            if task == FlightType.AIR_ASSAULT and not self.game.settings.plugin_option(
                "ctld"
            ):
                # Only add Air Assault if ctld plugin is enabled
                continue

            def make_closure(arg):
                def closure():
                    return self.confirm_recreate(arg)

                return closure

            button = QPushButton(f"Recreate as {task}")
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
        waypoints = []
        for (
            selected_row
        ) in self.flight_waypoint_list.selectionModel().selectedIndexes():
            if selected_row.row() > 0:
                waypoints.append(self.flight.flight_plan.waypoints[selected_row.row()])
        for waypoint in waypoints:
            self.delete_waypoint(waypoint)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def delete_waypoint(self, waypoint: FlightWaypoint) -> None:
        # Need to degrade to a custom flight plan and remove the waypoint.
        # If the waypoint is a target waypoint and is not the last target
        # waypoint, we don't need to degrade.
        if isinstance(self.flight.flight_plan, FormationAttackFlightPlan):
            is_target = waypoint in self.flight.flight_plan.targets
            if is_target and len(self.flight.flight_plan.targets) > 1:
                self.flight.flight_plan.targets.remove(waypoint)
                return

        self.degrade_to_custom_flight_plan()
        assert isinstance(self.flight.flight_plan, CustomFlightPlan)
        self.flight.flight_plan.layout.custom_waypoints.remove(waypoint)

    def on_fast_waypoint(self):
        self.subwindow = QPredefinedWaypointSelectionWindow(
            self.game, self.flight, self.flight_waypoint_list
        )
        self.subwindow.waypoints_added.connect(self.on_waypoints_added)
        self.subwindow.show()

    def on_waypoints_added(self, waypoints: Iterable[FlightWaypoint]) -> None:
        if not waypoints:
            return
        self.degrade_to_custom_flight_plan()
        assert isinstance(self.flight.flight_plan, CustomFlightPlan)
        self.flight.flight_plan.layout.custom_waypoints.extend(waypoints)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def on_rtb_waypoint(self):
        rtb = self.planner.generate_rtb_waypoint(self.flight, self.flight.from_cp)
        self.degrade_to_custom_flight_plan()
        assert isinstance(self.flight.flight_plan, CustomFlightPlan)
        self.flight.flight_plan.layout.custom_waypoints.append(rtb)
        self.flight_waypoint_list.update_list()
        self.on_change()

    def degrade_to_custom_flight_plan(self) -> None:
        if not isinstance(self.flight.flight_plan, CustomFlightPlan):
            self.flight.flight_plan = CustomFlightPlan(
                self.flight,
                CustomLayout(custom_waypoints=self.flight.flight_plan.waypoints),
            )

    def confirm_recreate(self, task: FlightType) -> None:
        result = QMessageBox.question(
            self,
            "Regenerate flight?",
            (
                "Changing the flight type will reset its flight plan. Do you want "
                "to continue?"
            ),
            QMessageBox.No,
            QMessageBox.Yes,
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
            if not self.flight.loadout.is_custom:
                self.flight.loadout = Loadout.default_for(self.flight)
                self.loadout_changed.emit()
            self.flight_waypoint_list.update_list()
            self.on_change()

    def on_change(self):
        self.flight_waypoint_list.update_list()
