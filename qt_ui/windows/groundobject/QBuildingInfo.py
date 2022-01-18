import os

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel
from game.db import REWARDS
from game.theater import GroundUnit


class QBuildingInfo(QGroupBox):
    def __init__(self, building, ground_object):
        super(QBuildingInfo, self).__init__()
        self.building: GroundUnit = building
        self.ground_object = ground_object
        self.init_ui()

    def init_ui(self):
        self.header = QLabel()
        path = os.path.join(
            "./resources/ui/units/buildings/" + self.building.type + ".png"
        )
        if not self.building.alive:
            pixmap = QPixmap("./resources/ui/units/buildings/dead.png")
        elif os.path.isfile(path):
            pixmap = QPixmap(path)
        else:
            pixmap = QPixmap("./resources/ui/units/buildings/missing.png")
        self.header.setPixmap(pixmap)
        name = "<b>{}</b> {}".format(
            self.building.type[0:18],
            "[DEAD]" if not self.building.alive else "",
        )
        self.name = QLabel(name)
        self.name.setProperty("style", "small")
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.name)

        if self.ground_object.category in REWARDS.keys():
            income_label_text = (
                "Value: " + str(REWARDS[self.ground_object.category]) + "M"
            )
            if not self.building.alive:
                income_label_text = "<s>" + income_label_text + "</s>"
            self.reward = QLabel(income_label_text)
            layout.addWidget(self.reward)

        footer = QHBoxLayout()
        self.setLayout(layout)
