from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox

from qt_ui.uiconstants import VEHICLES_ICONS
from theater import ControlPoint, TheaterGroundObject


class QBaseDefenseGroupInfo(QGroupBox):

    def __init__(self, cp:ControlPoint, ground_object: TheaterGroundObject):
        super(QBaseDefenseGroupInfo, self).__init__("Group : " + ground_object.obj_name)
        self.ground_object = ground_object
        self.init_ui()

    def init_ui(self):
        unit_dict = {}
        layout = QGridLayout()
        for g in self.ground_object.groups:
            for u in g.units:
                if u.type in unit_dict.keys():
                    unit_dict[u.type] = unit_dict[u.type] + 1
                else:
                    unit_dict[u.type] = 1
        i = 0
        for k, v in unit_dict.items():
            icon = QLabel()
            if k in VEHICLES_ICONS.keys():
                icon.setPixmap(VEHICLES_ICONS[k])
            else:
                icon.setText("<b>" + k[:6] + "</b>")
            icon.setProperty("style", "icon-plane")
            layout.addWidget(icon, i, 0)
            layout.addWidget(QLabel(str(v) + " x " + k), i, 1)
            i = i + 1
        self.setLayout(layout)


