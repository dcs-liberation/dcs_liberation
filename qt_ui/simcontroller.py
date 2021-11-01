from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Optional, TYPE_CHECKING

from PySide2.QtCore import QObject, Signal

from game.sim.gameloop import GameLoop
from game.sim.simspeedsetting import SimSpeedSetting
from game.polldebriefingfilethread import PollDebriefingFileThread

if TYPE_CHECKING:
    from game import Game
    from game.debriefing import Debriefing


class SimController(QObject):
    sim_speed_reset = Signal(SimSpeedSetting)
    simulation_complete = Signal()

    def __init__(self, game: Optional[Game]) -> None:
        super().__init__()
        self.game_loop: Optional[GameLoop] = None
        self.recreate_game_loop(game)
        self.started = False

    @property
    def completed(self) -> bool:
        return self.game_loop.completed

    def set_game(self, game: Optional[Game]) -> None:
        self.recreate_game_loop(game)
        self.sim_speed_reset.emit(SimSpeedSetting.PAUSED)

    def recreate_game_loop(self, game: Optional[Game]) -> None:
        if self.game_loop is not None:
            self.game_loop.pause()
        if game is not None:
            self.game_loop = GameLoop(game, self.on_simulation_complete)
        self.started = False

    def set_simulation_speed(self, simulation_speed: SimSpeedSetting) -> None:
        if self.game_loop.completed and simulation_speed is not SimSpeedSetting.PAUSED:
            logging.debug("Cannot unpause sim: already complete")
            return
        if not self.started and simulation_speed is not SimSpeedSetting.PAUSED:
            self.game_loop.start()
            self.started = True
        self.game_loop.set_simulation_speed(simulation_speed)

    def run_to_first_contact(self) -> None:
        self.game_loop.run_to_first_contact()

    def generate_miz(self, output: Path) -> None:
        self.game_loop.pause_and_generate_miz(output)

    def wait_for_debriefing(
        self, callback: Callable[[Debriefing], None]
    ) -> PollDebriefingFileThread:
        thread = PollDebriefingFileThread(callback, self.game_loop.sim)
        thread.start()
        return thread

    def debrief_current_state(
        self, state_path: Path, force_end: bool = False
    ) -> Debriefing:
        return self.game_loop.pause_and_debrief(state_path, force_end)

    def process_results(self, debriefing: Debriefing) -> None:
        return self.game_loop.complete_with_results(debriefing)

    def on_simulation_complete(self) -> None:
        logging.debug("Simulation complete")
        self.simulation_complete.emit()
