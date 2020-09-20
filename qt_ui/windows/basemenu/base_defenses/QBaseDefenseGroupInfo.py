from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox, QPushButton

from qt_ui.uiconstants import VEHICLES_ICONS
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu
from theater import ControlPoint, TheaterGroundObject


class QBaseDefenseGroupInfo(QGroupBox):

    def __init__(self, cp:ControlPoint, ground_object: TheaterGroundObject, game):
        super(QBaseDefenseGroupInfo, self).__init__("Group : " + ground_object.obj_name)
        self.ground_object = ground_object
        self.cp = cp
        self.game = game
        self.buildings = game.theater.find_ground_objects_by_obj_name(self.ground_object.obj_name)
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
                icon.setText("<b>" + k[:9] + "</b>")
            icon.setProperty("style", "icon-armor")
            layout.addWidget(icon, i, 0)
            layout.addWidget(QLabel(str(v) + " x " + "<strong>" + k + "</strong>"), i, 1)
            i = i + 1

        manage_button = QPushButton("Manage")
        manage_button.setProperty("style", "btn-success")
        manage_button.setMaximumWidth(180)
        manage_button.clicked.connect(self.onManage)
        layout.addWidget(manage_button, i, 0, Qt.AlignLeft)
        self.setLayout(layout)

    def onManage(self):
        self.editionMenu = QGroundObjectMenu(self.window(), self.ground_object, self.buildings, self.cp, self.game)
        self.editionMenu.show()


