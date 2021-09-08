from PySide2.QtWidgets import QTabWidget

from game.theater import ControlPoint, Fob
from qt_ui.models import GameModel
from qt_ui.windows.basemenu.DepartingConvoysMenu import DepartingConvoysMenu
from qt_ui.windows.basemenu.airfield.QAirfieldCommand import QAirfieldCommand
from qt_ui.windows.basemenu.ground_forces.QGroundForcesHQ import QGroundForcesHQ
from qt_ui.windows.basemenu.intel.QIntelInfo import QIntelInfo


class QBaseMenuTabs(QTabWidget):
    def __init__(self, cp: ControlPoint, game_model: GameModel):
        super(QBaseMenuTabs, self).__init__()

        if not cp.captured:
            self.intel = QIntelInfo(cp)
            self.addTab(self.intel, "Intel")

            self.departing_convoys = DepartingConvoysMenu(cp, game_model)
            self.addTab(self.departing_convoys, "Departing Convoys")
            return

        if isinstance(cp, Fob):
            self.ground_forces_hq = QGroundForcesHQ(cp, game_model)
            self.addTab(self.ground_forces_hq, "Ground Forces HQ")
            if cp.helipads:
                self.airfield_command = QAirfieldCommand(cp, game_model)
                self.addTab(self.airfield_command, "Heliport")
        else:
            self.airfield_command = QAirfieldCommand(cp, game_model)
            self.addTab(self.airfield_command, "Airfield Command")
            if cp.can_deploy_ground_units:
                self.ground_forces_hq = QGroundForcesHQ(cp, game_model)
                self.addTab(self.ground_forces_hq, "Ground Forces HQ")
