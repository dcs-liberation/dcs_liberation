from PySide2.QtWidgets import QLabel, QGroupBox, QVBoxLayout

from game import Game
from qt_ui.windows.basemenu.ground_forces.QGroundForcesStrategySelector import QGroundForcesStrategySelector
from theater import ControlPoint


class QGroundForcesStrategy(QGroupBox):

    def __init__(self, cp:ControlPoint, game:Game):
        super(QGroundForcesStrategy, self).__init__("Frontline operations :")
        self.cp = cp
        self.game = game
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        for enemy_cp in self.cp.connected_points:
            if not enemy_cp.captured:
                layout.addWidget(QLabel(enemy_cp.name))
                layout.addWidget(QGroundForcesStrategySelector(self.cp, enemy_cp))
        layout.addStretch()
        self.setLayout(layout)
