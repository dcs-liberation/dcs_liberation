from PySide2.QtGui import Qt
from PySide2.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QGroupBox
from dcs import Point

from game import Game
from game.utils import meter_to_nm
from gen.flights.flight import Flight
from qt_ui.widgets.combos.QPredefinedWaypointSelectionComboBox import QPredefinedWaypointSelectionComboBox
from qt_ui.windows.mission.flight.generator.QAbstractMissionGenerator import QAbstractMissionGenerator


class QCASMissionGenerator(QAbstractMissionGenerator):

    def __init__(self, game: Game, flight: Flight, flight_waypoint_list):
        super(QCASMissionGenerator, self).__init__(game, flight, flight_waypoint_list, "CAS Generator")

        self.wpt_selection_box = QPredefinedWaypointSelectionComboBox(self.game, self, False, False, True, False, False)
        self.wpt_selection_box.setMinimumWidth(200)
        self.wpt_selection_box.currentTextChanged.connect(self.on_select_wpt_changed)

        self.distanceToTargetLabel = QLabel("0 nm")
        self.init_ui()
        self.on_select_wpt_changed()

    def on_select_wpt_changed(self):
        super(QCASMissionGenerator, self).on_select_wpt_changed()
        wpts = self.wpt_selection_box.get_selected_waypoints()

        if len(wpts) > 0:
            self.distanceToTargetLabel.setText("~" + str(meter_to_nm(self.flight.from_cp.position.distance_to_point(Point(wpts[0].x, wpts[0].y)))) + " nm")
        else:
            self.distanceToTargetLabel.setText("??? nm")

    def init_ui(self):
        layout = QVBoxLayout()

        wpt_layout = QHBoxLayout()
        wpt_layout.addWidget(QLabel("CAS : "))
        wpt_layout.addWidget(self.wpt_selection_box)
        wpt_layout.addStretch()

        distToTargetBox = QGroupBox("Infos :")
        distToTarget = QHBoxLayout()
        distToTarget.addWidget(QLabel("Distance to target : "))
        distToTarget.addStretch()
        distToTarget.addWidget(self.distanceToTargetLabel, alignment=Qt.AlignRight)
        distToTargetBox.setLayout(distToTarget)

        layout.addLayout(wpt_layout)
        layout.addWidget(self.wpt_info)
        layout.addWidget(distToTargetBox)
        layout.addStretch()
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def apply(self):
        self.flight.points = []
        self.planner.generate_cas(self.flight, self.selected_waypoints[0].data[0], self.selected_waypoints[0].data[1])
        self.flight_waypoint_list.update_list()
        self.close()




