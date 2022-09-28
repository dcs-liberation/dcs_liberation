from PySide2.QtWidgets import QFrame, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout

from game.theater import ControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.airfield.QAircraftRecruitmentMenu import (
    QAircraftRecruitmentMenu,
)
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView


class QAirfieldCommand(QFrame):
    def __init__(self, cp: ControlPoint, game_model: GameModel):
        super(QAirfieldCommand, self).__init__()
        self.cp = cp
        self.game_model = game_model
        self.init_ui()

    def init_ui(self):
        wrapper_layout = QVBoxLayout()
        layout = QHBoxLayout()
        wrapper_layout.addLayout(layout)

        layout.addWidget(QAircraftRecruitmentMenu(self.cp, self.game_model), stretch=5)

        planned = QGroupBox("Planned Flights")
        planned_layout = QVBoxLayout()
        planned_layout.addWidget(QPlannedFlightsView(self.game_model, self.cp))
        planned.setLayout(planned_layout)
        layout.addWidget(planned, stretch=3)

        wrapper_layout.addWidget(
            QLabel(
                "Purchasing aircraft at this airbase requires squadrons to be present. "
                "To transfer additional squadrons to this airbase, open<br />"
                "the air wing menu, double click the squadron to transfer, then select "
                "the transfer destination."
            )
        )

        self.setLayout(wrapper_layout)
