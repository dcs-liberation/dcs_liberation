from collections.abc import Callable

from PySide2.QtWidgets import QGroupBox, QLabel, QPushButton, QVBoxLayout

from game import Game
from game.server import EventStream
from game.sim.gameupdateevents import GameUpdateEvents
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
        front_line = self.cp.front_line_with(enemy_point)
        front_line.update_position()
        events = GameUpdateEvents().update_front_line(front_line)
        # Clear the ATO to replan missions affected by the front line.
        self.game.initialize_turn(events)
        EventStream.put_nowait(events)
        GameUpdateSignal.get_instance().updateGame(self.game)
