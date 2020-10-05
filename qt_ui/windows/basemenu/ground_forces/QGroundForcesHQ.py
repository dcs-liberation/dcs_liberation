from PySide2.QtWidgets import QFrame, QGridLayout

from qt_ui.models import GameModel
from qt_ui.windows.basemenu.ground_forces.QArmorRecruitmentMenu import \
    QArmorRecruitmentMenu
from qt_ui.windows.basemenu.ground_forces.QGroundForcesStrategy import \
    QGroundForcesStrategy
from theater import ControlPoint


class QGroundForcesHQ(QFrame):

    def __init__(self, cp: ControlPoint, game_model: GameModel) -> None:
        super(QGroundForcesHQ, self).__init__()
        self.cp = cp
        self.game_model = game_model
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        layout.addWidget(QArmorRecruitmentMenu(self.cp, self.game_model), 0, 0)
        layout.addWidget(QGroundForcesStrategy(self.cp, self.game_model.game),
                         0, 1)
        self.setLayout(layout)
