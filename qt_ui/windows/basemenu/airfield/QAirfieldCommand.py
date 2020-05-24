from PySide2.QtWidgets import QFrame, QGridLayout, QLabel, QHBoxLayout, QGroupBox, QVBoxLayout
from game import Game
from qt_ui.widgets.base.QAirportInformation import QAirportInformation
from qt_ui.windows.basemenu.airfield.QAircraftRecruitmentMenu import QAircraftRecruitmentMenu
from qt_ui.windows.mission.QPlannedFlightsView import QPlannedFlightsView
from theater import ControlPoint


class QAirfieldCommand(QFrame):

    def __init__(self, cp:ControlPoint, game:Game):
        super(QAirfieldCommand, self).__init__()
        self.cp = cp
        self.game = game
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(QAircraftRecruitmentMenu(self.cp, self.game), 0, 0)

        try:
            planned = QGroupBox("Planned Flights")
            planned_layout = QVBoxLayout()
            planned_layout.addWidget(QPlannedFlightsView(self.game.planners[self.cp.id]))
            planned.setLayout(planned_layout)
            layout.addWidget(planned, 0, 1)
        except:
            pass

        #layout.addWidget(QAirportInformation(self.cp, self.game.theater.terrain.airport_by_id(self.cp.id)), 0, 2)
        self.setLayout(layout)
