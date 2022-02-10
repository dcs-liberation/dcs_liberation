import os

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QVBoxLayout
from game.theater import TheaterUnit

from game.config import REWARDS


class QBuildingInfo(QGroupBox):
    def __init__(self, building: TheaterUnit, ground_object):
        super(QBuildingInfo, self).__init__()
        self.building = building
        self.ground_object = ground_object
        self.init_ui()

    def init_ui(self):
        self.header = QLabel()
        path = os.path.join(
            "./resources/ui/units/buildings/" + self.building.icon + ".png"
        )
        if not self.building.alive:
            pixmap = QPixmap("./resources/ui/units/buildings/dead.png")
        elif os.path.isfile(path):
            pixmap = QPixmap(path)
        else:
            pixmap = QPixmap("./resources/ui/units/buildings/missing.png")
        self.header.setPixmap(pixmap)
        self.name = QLabel(self.building.short_name)
        self.name.setProperty("style", "small")
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addWidget(self.name)

        if self.ground_object.category in REWARDS:
            income_label_text = (
                "Value: " + str(REWARDS[self.ground_object.category]) + "M"
            )
            if not self.building.alive:
                income_label_text = "<s>" + income_label_text + "</s>"
            self.reward = QLabel(income_label_text)
            layout.addWidget(self.reward)

        footer = QHBoxLayout()
        self.setLayout(layout)
