from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from game import Game
from game.ato.flight import Flight
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.widgets.combos.QPredefinedWaypointSelectionComboBox import (
    QPredefinedWaypointSelectionComboBox,
)
from qt_ui.windows.mission.flight.waypoints.QFlightWaypointInfoBox import (
    QFlightWaypointInfoBox,
)

PREDEFINED_WAYPOINT_CATEGORIES = [
    "Frontline (CAS AREA)",
    "Building",
    "Units",
    "Airbase",
]


class QPredefinedWaypointSelectionWindow(QDialog):

    # List of FlightWaypoint
    waypoints_added = Signal(list)

    def __init__(self, game: Game, flight: Flight, flight_waypoint_list):
        super(QPredefinedWaypointSelectionWindow, self).__init__()
        self.game = game
        self.flight = flight
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(400, 250)
        self.setModal(True)
        self.setWindowTitle("Add Predefined Waypoint")
        self.setWindowIcon(EVENT_ICONS["strike"])
        self.flight_waypoint_list = flight_waypoint_list

        self.wpt_selection_box = QPredefinedWaypointSelectionComboBox(self.game)
        self.wpt_selection_box.setMinimumWidth(200)
        self.wpt_selection_box.currentTextChanged.connect(self.on_select_wpt_changed)
        self.selected_waypoints = []
        self.wpt_info = QFlightWaypointInfoBox()

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_waypoint)

        self.include_all = QCheckBox()
        self.include_all.stateChanged.connect(self.on_select_wpt_changed)
        self.include_all.setChecked(True)

        self.init_ui()
        self.on_select_wpt_changed()

    def init_ui(self):
        layout = QVBoxLayout()

        wpt_layout = QHBoxLayout()
        wpt_layout.addWidget(QLabel("Waypoint : "))
        wpt_layout.addWidget(self.wpt_selection_box)
        wpt_layout.addStretch()

        include_all = QHBoxLayout()
        include_all.addWidget(QLabel("Include all objects from the same location : "))
        include_all.addWidget(self.include_all)
        include_all.addStretch()

        layout.addLayout(wpt_layout)
        layout.addWidget(self.wpt_info)
        layout.addLayout(include_all)
        layout.addStretch()
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def on_select_wpt_changed(self):
        self.selected_waypoints = self.wpt_selection_box.get_selected_waypoints(
            self.include_all.isChecked()
        )
        if self.selected_waypoints is None or len(self.selected_waypoints) <= 0:
            self.add_button.setDisabled(True)
        else:
            self.wpt_info.set_flight_waypoint(self.selected_waypoints[0])
            self.add_button.setDisabled(False)

    def add_waypoint(self):
        self.waypoints_added.emit(self.selected_waypoints)
        self.close()
