from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from qt_ui.windows.newgame.QNewGameWizard import NewGameWizard


class GameOverDialog(QDialog):
    def __init__(self, won: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Game Over")

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(
            QLabel(
                f"<strong>You {'won' if won else 'lost'}!</strong><br />"
                "<br />"
                "Click below to start a new game."
            )
        )
        button_row = QHBoxLayout()
        layout.addLayout(button_row)

        button_row.addStretch()

        new_game = QPushButton("New Game")
        new_game.clicked.connect(self.on_new_game)
        button_row.addWidget(new_game)

    def on_new_game(self) -> None:
        wizard = NewGameWizard(self)
        wizard.show()
        wizard.accepted.connect(self.accept)
