import logging

from PySide2.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

from game import Game
from gen.ato import Package
from gen.flights.flight import Flight, FlightType
from qt_ui.widgets.combos.QPredefinedWaypointSelectionComboBox import QPredefinedWaypointSelectionComboBox
from qt_ui.windows.mission.flight.generator.QAbstractMissionGenerator import QAbstractMissionGenerator
from theater import ControlPoint, FrontLine


class QCAPMissionGenerator(QAbstractMissionGenerator):

    def __init__(self, game: Game, package: Package, flight: Flight,
                 flight_waypoint_list) -> None:
        super(QCAPMissionGenerator, self).__init__(
            game,
            package,
            flight,
            flight_waypoint_list,
            "CAP Generator"
        )

        self.wpt_selection_box = QPredefinedWaypointSelectionComboBox(self.game, self, False, True, True, False, False, True)
        self.wpt_selection_box.setMinimumWidth(200)
        self.wpt_selection_box.currentTextChanged.connect(self.on_select_wpt_changed)

        self.init_ui()
        self.on_select_wpt_changed()

    def init_ui(self):
        layout = QVBoxLayout()

        wpt_layout = QHBoxLayout()
        wpt_layout.addWidget(QLabel("CAP mission on : "))
        wpt_layout.addWidget(self.wpt_selection_box)
        wpt_layout.addStretch()

        layout.addLayout(wpt_layout)
        layout.addWidget(self.wpt_info)
        layout.addStretch()
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def apply(self):
        location = self.package.target
        if isinstance(location, FrontLine):
            self.flight.flight_type = FlightType.TARCAP
            self.planner.populate_flight_plan(self.flight)
        elif isinstance(location, ControlPoint):
            if location.is_fleet:
                self.flight.flight_type = FlightType.BARCAP
            else:
                self.flight.flight_type = FlightType.CAP
        else:
            name = location.__class__.__name__
            logging.error(f"Unexpected objective type for CAP: {name}")
            return

        self.planner.generate_barcap(self.flight)

        self.flight_waypoint_list.update_list()
        self.close()




