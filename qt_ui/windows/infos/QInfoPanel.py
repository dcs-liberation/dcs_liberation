from PySide2.QtWidgets import QFrame, QVBoxLayout, QLabel, QGroupBox

from game import Game
from qt_ui.windows.infos.QInfoList import QInfoList


class QInfoPanel(QGroupBox):
    def __init__(self, game: Game):
        super(QInfoPanel, self).__init__("Info Panel")
        self.informations_list = QInfoList(game)
        self.init_ui()

    def setGame(self, game):
        self.game = game
        self.informations_list.setGame(game)

    def update(self):
        self.informations_list.update_list()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.informations_list)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 20, 0, 0)
        self.setLayout(layout)
