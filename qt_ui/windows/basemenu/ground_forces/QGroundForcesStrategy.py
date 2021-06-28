from collections import Callable
from datetime import timedelta

from PySide2.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QPushButton, QTimeEdit
from PySide2.QtCore import QTime

from game import Game
from game.theater import ControlPoint
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.ground_forces.QGroundForcesStrategySelector import (
    QGroundForcesStrategySelector,
)


class QGroundForcesStrategy(QGroupBox):
    def __init__(self, cp: ControlPoint, game: Game):
        super(QGroundForcesStrategy, self).__init__("Frontline operations :")
        self.cp = cp
        self.game = game
        self.init_ui()

    def init_ui(self):
        def make_cheat_callback(
            enemy_point: ControlPoint, advance: bool
        ) -> Callable[[], None]:
            def cheat() -> None:
                self.cheat_alter_front_line(enemy_point, advance)

            return cheat

        layout = QVBoxLayout()
        for enemy_cp in self.cp.connected_points:
            if not enemy_cp.captured:
                layout.addWidget(QLabel(enemy_cp.name))
                layout.addWidget(QGroundForcesStrategySelector(self.cp, enemy_cp))

                layout.addWidget(QLabel("Delay movement until"))
                self.delayed_start_spinner = QTimeEdit()
                self.delayed_start_spinner.setMinimumTime(QTime(0, 0))
                self.delayed_start_spinner.setDisplayFormat("T+hh:mm:ss")
                self.delayed_start_spinner.timeChanged.connect(self.save_delayed_start)
                self.delayed_start_spinner.setToolTip(
                    "Forces will not move from Waypoint 1 until the specified time has elapsed."
                )
                self.delayed_start_spinner.setStyleSheet("background: #1D2731;")
                layout.addWidget(self.delayed_start_spinner)

                if self.game.settings.enable_frontline_cheats:
                    advance_button = QPushButton("CHEAT: Advance")
                    advance_button.setProperty("style", "btn-danger")
                    layout.addWidget(advance_button)
                    advance_button.clicked.connect(
                        make_cheat_callback(enemy_cp, advance=True)
                    )

                    retreat_button = QPushButton("CHEAT: Retreat")
                    retreat_button.setProperty("style", "btn-danger")
                    layout.addWidget(retreat_button)
                    retreat_button.clicked.connect(
                        make_cheat_callback(enemy_cp, advance=False)
                    )

        layout.addStretch()
        self.setLayout(layout)

    def cheat_alter_front_line(self, enemy_point: ControlPoint, advance: bool) -> None:
        amount = 0.2
        if not advance:
            amount *= -1
        self.cp.base.affect_strength(amount)
        enemy_point.base.affect_strength(-amount)
        # Clear the ATO to replan missions affected by the front line.
        self.game.reset_ato()
        self.game.initialize_turn()
        GameUpdateSignal.get_instance().updateGame(self.game)

    def save_delayed_start(self) -> None:
        time = self.delayed_start_spinner.time()
        seconds = time.hour() * 3600 + time.minute() * 60 + time.second()
        self.cp.delayed_start = timedelta(seconds=seconds)
