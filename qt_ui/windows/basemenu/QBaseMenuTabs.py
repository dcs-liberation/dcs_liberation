from PySide2.QtWidgets import QTabWidget, QFrame, QGridLayout, QLabel

from game import Game
from qt_ui.windows.basemenu.airfield.QAirfieldCommand import QAirfieldCommand
from qt_ui.windows.basemenu.base_defenses.QBaseDefensesHQ import QBaseDefensesHQ
from qt_ui.windows.basemenu.ground_forces.QGroundForcesHQ import QGroundForcesHQ
from qt_ui.windows.basemenu.intel.QIntelInfo import QIntelInfo
from theater import ControlPoint


class QBaseMenuTabs(QTabWidget):

    def __init__(self, cp: ControlPoint, game: Game):
        super(QBaseMenuTabs, self).__init__()
        self.cp = cp
        if cp:

            if not cp.captured:
                self.intel = QIntelInfo(cp, game)
                self.addTab(self.intel, "Intel")
                if not cp.is_carrier:
                    self.base_defenses_hq = QBaseDefensesHQ(cp, game)
                    self.addTab(self.base_defenses_hq, "Base Defenses")
            else:
                if cp.has_runway():
                    self.airfield_command = QAirfieldCommand(cp, game)
                    self.addTab(self.airfield_command, "Airfield Command")

                if not cp.is_carrier:
                    self.ground_forces_hq = QGroundForcesHQ(cp, game)
                    self.addTab(self.ground_forces_hq, "Ground Forces HQ")
                    self.base_defenses_hq = QBaseDefensesHQ(cp, game)
                    self.addTab(self.base_defenses_hq, "Base Defenses")
                else:
                    self.base_defenses_hq = QBaseDefensesHQ(cp, game)
                    self.addTab(self.base_defenses_hq, "Fleet")

        else:
            tabError = QFrame()
            l = QGridLayout()
            l.addWidget(QLabel("No Control Point"))
            tabError.setLayout(l)
            self.addTab(tabError, "No Control Point")