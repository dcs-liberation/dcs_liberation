from PySide2.QtWidgets import QFrame, QGridLayout
from game import Game
from qt_ui.windows.basemenu.base_defenses.QBaseInformation import QBaseInformation
from theater import ControlPoint


class QBaseDefensesHQ(QFrame):

    def __init__(self, cp:ControlPoint, game:Game):
        super(QBaseDefensesHQ, self).__init__()
        self.cp = cp
        self.game = game
        self.init_ui()

    def init_ui(self):
        airport = self.game.theater.terrain.airport_by_id(self.cp.id)
        layout = QGridLayout()
        layout.addWidget(QBaseInformation(self.cp, airport, self.game))
        self.setLayout(layout)

