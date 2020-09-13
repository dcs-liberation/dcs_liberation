from PySide2.QtWidgets import QFrame, QGridLayout, QGroupBox, QVBoxLayout

from qt_ui.models import GameModel
from qt_ui.windows.basemenu.airfield.QAircraftRecruitmentMenu import \
    QAircraftRecruitmentMenu
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView
from theater import ControlPoint


class QAirfieldCommand(QFrame):

    def __init__(self, cp:ControlPoint, game_model: GameModel):
        super(QAirfieldCommand, self).__init__()
        self.cp = cp
        self.game_model = game_model
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(QAircraftRecruitmentMenu(self.cp, self.game_model), 0, 0)

        try:
            planned = QGroupBox("Planned Flights")
            planned_layout = QVBoxLayout()
            planned_layout.addWidget(
                QPlannedFlightsView(self.game_model, self.cp)
            )
            planned.setLayout(planned_layout)
            layout.addWidget(planned, 0, 1)
        except:
            pass

        #layout.addWidget(QAirportInformation(self.cp, self.game.theater.terrain.airport_by_id(self.cp.id)), 0, 2)
        self.setLayout(layout)
