from PySide2.QtWidgets import QFrame, QGridLayout, QGroupBox, QVBoxLayout

from game.theater import ControlPoint
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.airfield.QAircraftRecruitmentMenu import \
    QAircraftRecruitmentMenu
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView


class QAirfieldCommand(QFrame):

    def __init__(self, cp:ControlPoint, game_model: GameModel):
        super(QAirfieldCommand, self).__init__()
        self.cp = cp
        self.game_model = game_model
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.setHorizontalSpacing(1)
        layout.addWidget(QAircraftRecruitmentMenu(self.cp, self.game_model), 0, 0)

        planned = QGroupBox("Planned Flights")
        planned_layout = QVBoxLayout()
        planned_layout.addWidget(
            QPlannedFlightsView(self.game_model, self.cp)
        )
        planned.setLayout(planned_layout)
        layout.addWidget(planned, 0, 1)

        self.setLayout(layout)
