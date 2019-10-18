from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout

from game import db
from qt_ui.uiconstants import AIRCRAFT_ICONS, VEHICLES_ICONS
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
            icon = QLabel()
            if k in VEHICLES_ICONS.keys():
                icon.setPixmap(VEHICLES_ICONS[k])
            else:
                icon.setText("<b>"+k[:6]+"</b>")
            icon.setProperty("style", "icon-plane")
            self.layout.addWidget(icon, i, 0)
            self.layout.addWidget(QLabel(str(v) + " x " + k), i, 1)
            i = i + 1

        stretch = QVBoxLayout()
        stretch.addStretch()
        self.layout.addLayout(stretch, len(unit_dict) + 1, 0)
        self.setLayout(self.layout)
