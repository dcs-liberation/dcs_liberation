from typing import Optional

from PySide2.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
)

from game import Game
from game.income import Income
from qt_ui.windows.intel import IntelWindow


class QIntelBox(QGroupBox):
    def __init__(self, game: Game) -> None:
        super().__init__("Intel")
        self.setProperty("style", "IntelSummary")

        self.game = game

        columns = QHBoxLayout()
        self.setLayout(columns)

        summary = QGridLayout()
        summary.setContentsMargins(5, 5, 5, 5)

        air_superiority = QLabel("Air superiority:")
        summary.addWidget(air_superiority, 0, 0)
        self.air_strength = QLabel()
        summary.addWidget(self.air_strength, 0, 1)

        front_line = QLabel("Front line:")
        summary.addWidget(front_line, 1, 0)
        self.ground_strength = QLabel()
        summary.addWidget(self.ground_strength, 1, 1)

        economy = QLabel("Economic strength:")
        summary.addWidget(economy, 2, 0)
        self.economic_strength = QLabel()
        summary.addWidget(self.economic_strength, 2, 1)

        self.details = QPushButton()
        self.details.setMinimumHeight(50)
        self.details.setMinimumWidth(210)
        self.details.setLayout(summary)
        columns.addWidget(self.details)
        self.details.clicked.connect(self.open_details_window)
        self.details.setEnabled(False)

        self.update_summary()

        self.details_window: Optional[IntelWindow] = None

    def set_game(self, game: Optional[Game]) -> None:
        self.game = game
        self.details.setEnabled(True)
        self.update_summary()

    @staticmethod
    def forces_strength_text(own: int, enemy: int) -> str:
        if not enemy:
            return "enemy eliminated"

        ratio = own / enemy
        if ratio < 0.6:
            return "outnumbered"
        if ratio < 0.8:
            return "slightly outnumbered"
        if ratio < 1.2:
            return "evenly matched"
        if ratio < 1.4:
            return "slight advantage"
        return "strong advantage"

    def economic_strength_text(self) -> str:
        assert self.game is not None
        own = Income(self.game, player=True).total
        enemy = Income(self.game, player=False).total

        if not enemy:
            return "enemy economy ruined"

        ratio = own / enemy
        if ratio < 0.6:
            return "strong disadvantage"
        if ratio < 0.8:
            return "slight disadvantage"
        if ratio < 1.2:
            return "evenly matched"
        if ratio < 1.4:
            return "slight advantage"
        return "strong advantage"

    def update_summary(self) -> None:
        if self.game is None:
            self.air_strength.setText("no data")
            self.ground_strength.setText("no data")
            self.economic_strength.setText("no data")
            return

        data = self.game.game_stats.data_per_turn[-1]

        self.air_strength.setText(
            self.forces_strength_text(
                data.allied_units.aircraft_count, data.enemy_units.aircraft_count
            )
        )
        self.ground_strength.setText(
            self.forces_strength_text(
                data.allied_units.vehicles_count, data.enemy_units.vehicles_count
            )
        )
        self.economic_strength.setText(self.economic_strength_text())

        if self.game.turn == 0:
            self.air_strength.setText("gathering intel")
            self.ground_strength.setText("gathering intel")

    def open_details_window(self) -> None:
        self.details_window = IntelWindow(self.game)
        self.details_window.show()
