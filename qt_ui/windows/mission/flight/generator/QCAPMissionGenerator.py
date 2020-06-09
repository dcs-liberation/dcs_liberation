from PySide2.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

from game import Game
from gen.flights.flight import Flight, PredefinedWaypointCategory
from qt_ui.widgets.combos.QPredefinedWaypointSelectionComboBox import QPredefinedWaypointSelectionComboBox
from qt_ui.windows.mission.flight.generator.QAbstractMissionGenerator import QAbstractMissionGenerator


class QCAPMissionGenerator(QAbstractMissionGenerator):

    def __init__(self, game: Game, flight: Flight, flight_waypoint_list):
        super(QCAPMissionGenerator, self).__init__(game, flight, flight_waypoint_list, "CAP Generator")

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
        self.flight.points = []

        wpt = self.selected_waypoints[0]
        if wpt.category == PredefinedWaypointCategory.FRONTLINE:
            self.planner.generate_frontline_cap(self.flight, wpt.data[0], wpt.data[1])
        elif wpt.category == PredefinedWaypointCategory.ALLY_CP:
            self.planner.generate_barcap(self.flight, wpt.data)
        else:
            return

        self.flight_waypoint_list.update_list()
        self.close()




