from PySide2.QtWidgets import QLabel, QGroupBox, QGridLayout
from game import Game


class QFactionsInfos(QGroupBox):
    """
    UI Component to display current turn and time info
    """

    def __init__(self, game):
        super(QFactionsInfos, self).__init__("Factions")

        self.player_name = QLabel("")
        self.enemy_name = QLabel("")
        self.setGame(game)

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.addWidget(QLabel("<b>Player : </b>"), 0, 0)
        self.layout.addWidget(self.player_name, 0, 1)
        self.layout.addWidget(QLabel("<b>Enemy : </b>"), 1, 0)
        self.layout.addWidget(self.enemy_name, 1, 1)
        self.setLayout(self.layout)

    def setGame(self, game: Game):
        if game is not None:
            self.player_name.setText(game.blue.faction.name)
            self.enemy_name.setText(game.red.faction.name)
        else:
            self.player_name.setText("")
            self.enemy_name.setText("")
