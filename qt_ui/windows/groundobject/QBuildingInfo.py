import os

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel


class QBuildingInfo(QGroupBox):

    def __init__(self, building, ground_object):
        super(QBuildingInfo, self).__init__()
        self.building = building
        self.ground_object = ground_object
        self.init_ui()

    def init_ui(self):
        self.header = QLabel()
        path = os.path.join("./resources/ui/units/buildings/" + self.building.dcs_identifier + ".png")
        if self.building.is_dead:
            pixmap = QPixmap("./resources/ui/units/buildings/dead.png")
        elif os.path.isfile(path):
            pixmap = QPixmap(path)
        else:
            pixmap = QPixmap("./resources/ui/units/buildings/missing.png")
        self.header.setPixmap(pixmap)
        name = "<b>{}</b> {}".format(self.building.dcs_identifier[0:18], "[DEAD]" if self.building.is_dead else "")
        self.name = QLabel(name)
        self.name.setProperty("style", "small")
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.name)
        footer = QHBoxLayout()
        self.setLayout(layout)

