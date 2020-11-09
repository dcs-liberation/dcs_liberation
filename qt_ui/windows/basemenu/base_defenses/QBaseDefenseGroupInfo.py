from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, QGroupBox, QPushButton, QVBoxLayout

from qt_ui.dialogs import Dialog
from qt_ui.uiconstants import VEHICLES_ICONS
from qt_ui.windows.groundobject.QGroundObjectMenu import QGroundObjectMenu
from theater import ControlPoint, TheaterGroundObject


class QBaseDefenseGroupInfo(QGroupBox):

    def __init__(self, cp: ControlPoint, ground_object: TheaterGroundObject, game):
        super(QBaseDefenseGroupInfo, self).__init__("Group : " + ground_object.obj_name)
        self.ground_object = ground_object
        self.cp = cp
        self.game = game
        self.buildings = game.theater.find_ground_objects_by_obj_name(self.ground_object.obj_name)

        self.main_layout = QVBoxLayout()
        self.unit_layout = QGridLayout()

        self.init_ui()

    def init_ui(self):

        self.buildLayout()
        self.main_layout.addLayout(self.unit_layout)
        if not self.cp.captured and not self.ground_object.is_dead:
            attack_button = QPushButton("Attack")
            attack_button.setProperty("style", "btn-danger")
            attack_button.setMaximumWidth(180)
            attack_button.clicked.connect(self.onAttack)
            self.main_layout.addWidget(attack_button, 0, Qt.AlignLeft)

        if self.cp.captured:
            manage_button = QPushButton("Manage")
            manage_button.setProperty("style", "btn-success")
            manage_button.setMaximumWidth(180)
            manage_button.clicked.connect(self.onManage)
            self.main_layout.addWidget(manage_button, 0, Qt.AlignLeft)

        self.setLayout(self.main_layout)

    def buildLayout(self):
        unit_dict = {}
        for i in range(self.unit_layout.rowCount()):
            for j in range(self.unit_layout.columnCount()):
                item = self.unit_layout.itemAtPosition(i, j)
                if item is not None and item.widget() is not None:
                    item.widget().setParent(None)
                    print("Remove " + str(i) + ", " + str(j))

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
                icon.setText("<b>" + k[:8] + "</b>")
            icon.setProperty("style", "icon-armor")
            self.unit_layout.addWidget(icon, i, 0)
            self.unit_layout.addWidget(QLabel(str(v) + " x " + "<strong>" + k + "</strong>"), i, 1)
            i = i + 1

        if len(unit_dict.items()) == 0:
            self.unit_layout.addWidget(QLabel("/"), 0, 0)



        self.setLayout(self.main_layout)
    
    def onAttack(self):
        Dialog.open_new_package_dialog(self.ground_object, parent=self.window())

    def onManage(self):
        self.edition_menu = QGroundObjectMenu(self.window(), self.ground_object, self.buildings, self.cp, self.game)
        self.edition_menu.show()
        self.edition_menu.changed.connect(self.onEdition)

    def onEdition(self):
        self.buildLayout()