import os

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel
from game.db import REWARDS


class QBuildingInfo(QGroupBox):
    def __init__(self, building, ground_object):
        super(QBuildingInfo, self).__init__()
        self.building = building
        self.ground_object = ground_object
        self.init_ui()

    def init_ui(self):
        self.header = QLabel()
        path = os.path.join(
            "./resources/ui/units/buildings/" + self.building.dcs_identifier + ".png"
        )
        if self.building.is_dead:
            pixmap = QPixmap("./resources/ui/units/buildings/dead.png")
        elif os.path.isfile(path):
            pixmap = QPixmap(path)
        else:
            pixmap = QPixmap("./resources/ui/units/buildings/missing.png")
        self.header.setPixmap(pixmap)
        name = "<b>{}</b> {}".format(
            self.building.dcs_identifier[0:18],
            "[DEAD]" if self.building.is_dead else "",
        )
        self.name = QLabel(name)
        self.name.setProperty("style", "small")
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.name)

        if self.building.category in REWARDS.keys():
            income_label_text = "Value: " + str(REWARDS[self.building.category]) + "M"
            if self.building.is_dead:
                income_label_text = "<s>" + income_label_text + "</s>"
            self.reward = QLabel(income_label_text)
            layout.addWidget(self.reward)

        footer = QHBoxLayout()
        self.setLayout(layout)
