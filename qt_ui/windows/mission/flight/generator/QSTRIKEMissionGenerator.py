from PySide2.QtGui import Qt
from PySide2.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QGroupBox

from game import Game
from game.utils import meter_to_nm
from gen.flights.flight import Flight
from qt_ui.widgets.combos.QStrikeTargetSelectionComboBox import QStrikeTargetSelectionComboBox
from qt_ui.widgets.views.QStrikeTargetInfoView import QStrikeTargetInfoView
from qt_ui.windows.mission.flight.generator.QAbstractMissionGenerator import QAbstractMissionGenerator


class QSTRIKEMissionGenerator(QAbstractMissionGenerator):

    def __init__(self, game: Game, flight: Flight, flight_waypoint_list):
        super(QSTRIKEMissionGenerator, self).__init__(game, flight, flight_waypoint_list, "SEAD/DEAD Generator")

        self.tgt_selection_box = QStrikeTargetSelectionComboBox(self.game)
        self.tgt_selection_box.setMinimumWidth(200)
        self.tgt_selection_box.currentTextChanged.connect(self.on_selected_target_changed)


        self.distanceToTargetLabel = QLabel("0 nm")
        self.strike_infos = QStrikeTargetInfoView(None)
        self.init_ui()
        self.on_selected_target_changed()

    def on_selected_target_changed(self):
        target = self.tgt_selection_box.get_selected_target()
        self.distanceToTargetLabel.setText("~" + str(meter_to_nm(self.flight.from_cp.position.distance_to_point(target.location.position))) + " nm")
        self.strike_infos.setTarget(target)

    def init_ui(self):
        layout = QVBoxLayout()

        wpt_layout = QHBoxLayout()
        wpt_layout.addWidget(QLabel("SEAD/DEAD target : "))
        wpt_layout.addStretch()
        wpt_layout.addWidget(self.tgt_selection_box, alignment=Qt.AlignRight)

        distToTargetBox = QGroupBox("Infos :")
        distToTarget = QHBoxLayout()
        distToTarget.addWidget(QLabel("Distance to target : "))
        distToTarget.addStretch()
        distToTarget.addWidget(self.distanceToTargetLabel, alignment=Qt.AlignRight)
        distToTargetBox.setLayout(distToTarget)

        layout.addLayout(wpt_layout)
        layout.addWidget(self.strike_infos)
        layout.addWidget(distToTargetBox)
        layout.addStretch()
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def apply(self):
        self.flight.points = []
        target = self.tgt_selection_box.get_selected_target()
        self.planner.generate_strike(self.flight, target.location)
        self.flight_waypoint_list.update_list()
        self.close()




