from PySide2.QtWidgets import QFrame, QGridLayout, QLabel
from game import Game
from qt_ui.widgets.base.QBaseInformation import QBaseInformation
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
        layout.addWidget(QBaseInformation(self.cp, airport))
        self.setLayout(layout)

