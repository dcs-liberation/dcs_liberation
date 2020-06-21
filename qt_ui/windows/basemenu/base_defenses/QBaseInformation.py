from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QFrame

from game import db
from qt_ui.uiconstants import AIRCRAFT_ICONS, VEHICLES_ICONS
from qt_ui.windows.basemenu.base_defenses.QBaseDefenseGroupInfo import QBaseDefenseGroupInfo
from theater import ControlPoint, Airport


class QBaseInformation(QFrame):

    def __init__(self, cp:ControlPoint, airport:Airport):
        super(QBaseInformation, self).__init__()
        self.cp = cp
        self.airport = airport
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        for g in self.cp.ground_objects:
            if g.airbase_group:
                group_info = QBaseDefenseGroupInfo(self.cp, g)
                self.layout.addWidget(group_info)
        self.setLayout(self.layout)
