from PySide2.QtWidgets import (
    QDialog,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PySide2.QtGui import QTextCursor
from PySide2.QtCore import QTimer

import qt_ui.uiconstants as CONST
from game.game import Game

from time import sleep


class QNotesWindow(QDialog):
    def __init__(self, game: Game):
        super(QNotesWindow, self).__init__()

        self.game = game
        self.setWindowTitle("Notes")
        self.setWindowIcon(CONST.ICONS["Notes"])
        self.setMinimumSize(400, 100)
        self.resize(600, 450)

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.vbox.addWidget(
            QLabel("Saved notes are available as a page in your kneeboard.")
        )

        self.textbox = QPlainTextEdit(self)
        try:
            self.textbox.setPlainText(self.game.notes)
            self.textbox.moveCursor(QTextCursor.End)
        except AttributeError:  # old save may not have game.notes
            pass
        self.textbox.move(10, 10)
        self.textbox.resize(600, 450)
        self.textbox.setStyleSheet("background: #1D2731;")
        self.vbox.addWidget(self.textbox)

        self.button_row = QHBoxLayout()
        self.vbox.addLayout(self.button_row)

        self.clear_button = QPushButton(self)
        self.clear_button.setText("CLEAR")
        self.clear_button.setProperty("style", "btn-primary")
        self.clear_button.clicked.connect(self.clearNotes)
        self.button_row.addWidget(self.clear_button)

        self.save_button = QPushButton(self)
        self.save_button.setText("SAVE")
        self.save_button.setProperty("style", "btn-success")
        self.save_button.clicked.connect(self.saveNotes)
        self.button_row.addWidget(self.save_button)

    def clearNotes(self) -> None:
        self.textbox.setPlainText("")

    def saveNotes(self) -> None:
        self.game.notes = self.textbox.toPlainText()
        self.save_button.setText("SAVED")
        QTimer.singleShot(5000, lambda: self.save_button.setText("SAVE"))
