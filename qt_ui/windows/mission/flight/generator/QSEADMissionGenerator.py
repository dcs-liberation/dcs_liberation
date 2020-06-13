from PySide2.QtGui import Qt
from PySide2.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QGroupBox

from game import Game
from game.utils import meter_to_nm
from gen.flights.flight import Flight
from qt_ui.widgets.combos.QSEADTargetSelectionComboBox import QSEADTargetSelectionComboBox
from qt_ui.widgets.views.QSeadTargetInfoView import QSeadTargetInfoView
from qt_ui.windows.mission.flight.generator.QAbstractMissionGenerator import QAbstractMissionGenerator


class QSEADMissionGenerator(QAbstractMissionGenerator):

    def __init__(self, game: Game, flight: Flight, flight_waypoint_list):
        super(QSEADMissionGenerator, self).__init__(game, flight, flight_waypoint_list, "SEAD/DEAD Generator")

        self.tgt_selection_box = QSEADTargetSelectionComboBox(self.game)
        self.tgt_selection_box.setMinimumWidth(200)
        self.tgt_selection_box.currentTextChanged.connect(self.on_selected_target_changed)

        self.distanceToTargetLabel = QLabel("0 nm")
        self.threatRangeLabel = QLabel("0 nm")
        self.detectionRangeLabel = QLabel("0 nm")
        self.seadTargetInfoView = QSeadTargetInfoView(None)
        self.init_ui()
        self.on_selected_target_changed()

    def on_selected_target_changed(self):
        target = self.tgt_selection_box.get_selected_target()
        if target is not None:
            self.distanceToTargetLabel.setText("~" + str(meter_to_nm(self.flight.from_cp.position.distance_to_point(target.location.position))) + " nm")
            self.threatRangeLabel.setText(str(meter_to_nm(target.threat_range)) + " nm")
            self.detectionRangeLabel.setText(str(meter_to_nm(target.detection_range)) + " nm")
            self.seadTargetInfoView.setTarget(target)

    def init_ui(self):
        layout = QVBoxLayout()

        wpt_layout = QHBoxLayout()
        wpt_layout.addWidget(QLabel("SEAD/DEAD target : "))
        wpt_layout.addStretch()
        wpt_layout.addWidget(self.tgt_selection_box, alignment=Qt.AlignRight)

        distThreatBox = QGroupBox("Infos :")
        threatLayout = QVBoxLayout()

        distToTarget = QHBoxLayout()
        distToTarget.addWidget(QLabel("Distance to site : "))
        distToTarget.addStretch()
        distToTarget.addWidget(self.distanceToTargetLabel, alignment=Qt.AlignRight)

        threatRangeLayout = QHBoxLayout()
        threatRangeLayout.addWidget(QLabel("Site threat range : "))
        threatRangeLayout.addStretch()
        threatRangeLayout.addWidget(self.threatRangeLabel, alignment=Qt.AlignRight)

        detectionRangeLayout = QHBoxLayout()
        detectionRangeLayout.addWidget(QLabel("Site radar detection range: "))
        detectionRangeLayout.addStretch()
        detectionRangeLayout.addWidget(self.detectionRangeLabel, alignment=Qt.AlignRight)

        threatLayout.addLayout(distToTarget)
        threatLayout.addLayout(threatRangeLayout)
        threatLayout.addLayout(detectionRangeLayout)
        distThreatBox.setLayout(threatLayout)

        layout.addLayout(wpt_layout)
        layout.addWidget(self.seadTargetInfoView)
        layout.addWidget(distThreatBox)
        layout.addStretch()
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def apply(self):
        self.flight.points = []
        target = self.tgt_selection_box.get_selected_target()
        self.planner.generate_sead(self.flight, target.location, target.radars)
        self.flight_waypoint_list.update_list()
        self.close()




