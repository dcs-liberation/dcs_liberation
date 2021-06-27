from PySide2.QtWidgets import QDialog, QLineEdit

import qt_ui.uiconstants as CONST
from game.game import Game


class QNotesWindow(QDialog):
    def __init__(self, game: Game):
        super(QNotesWindow, self).__init__()

        self.game = game
        self.setModal(True)
        self.setWindowTitle("Stats")
        self.setWindowIcon(CONST.ICONS["Notes"])
        self.setMinimumSize(600, 250)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
