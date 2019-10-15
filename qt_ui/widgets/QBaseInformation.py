from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox

from game import db
from theater import ControlPoint, Airport


class QBaseInformation(QGroupBox):

    def __init__(self, cp:ControlPoint, airport:Airport):
        super(QBaseInformation, self).__init__("Base defenses")
        self.cp = cp
        self.airport = airport
        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()

        unit_dict = {}
        for g in self.cp.ground_objects:
            if g.airbase_group:
                for group in g.groups:
                    for u in group.units:
                        if u.type in unit_dict.keys():
                            unit_dict[u.type] = unit_dict[u.type] + 1
                        else:
                            unit_dict[u.type] = 1

        i = 0
        for k,v in unit_dict.items():
            self.layout.addWidget(QLabel(str(v) + " x " + k), i, 0)
            i = i + 1

        self.setLayout(self.layout)
