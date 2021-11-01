from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, TYPE_CHECKING

from PySide2.QtCore import QObject, Signal

from game.polldebriefingfilethread import PollDebriefingFileThread
from game.sim.gameloop import GameLoop
from game.sim.simspeedsetting import SimSpeedSetting
from qt_ui.simupdatethread import SimUpdateThread

if TYPE_CHECKING:
    from game import Game
    from game.debriefing import Debriefing


class SimController(QObject):
    sim_update = Signal()
    sim_speed_reset = Signal(SimSpeedSetting)
    simulation_complete = Signal()

    def __init__(self, game: Optional[Game]) -> None:
        super().__init__()
        self.game_loop: Optional[GameLoop] = None
        self.recreate_game_loop(game)
        self.started = False
        self._sim_update_thread = SimUpdateThread(self.sim_update.emit)
        self._sim_update_thread.start()

    @property
    def completed(self) -> bool:
        return self.game_loop.completed

    @property
    def current_time_in_sim(self) -> Optional[datetime]:
        if self.game_loop is None:
            return None
        return self.game_loop.current_time_in_sim

    def set_game(self, game: Optional[Game]) -> None:
        self.recreate_game_loop(game)
        self.sim_speed_reset.emit(SimSpeedSetting.PAUSED)

    def recreate_game_loop(self, game: Optional[Game]) -> None:
        if self.game_loop is not None:
            self._sim_update_thread.on_sim_pause()
            self.game_loop.pause()
        self.game_loop = None
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
        if simulation_speed is SimSpeedSetting.PAUSED:
            self._sim_update_thread.on_sim_pause()
        else:
            self._sim_update_thread.on_sim_unpause()

    def run_to_first_contact(self) -> None:
        self.game_loop.run_to_first_contact()
        self.sim_update.emit()

    def generate_miz(self, output: Path) -> None:
        self._sim_update_thread.on_sim_pause()
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
        self._sim_update_thread.on_sim_pause()
        return self.game_loop.pause_and_debrief(state_path, force_end)

    def process_results(self, debriefing: Debriefing) -> None:
        self._sim_update_thread.on_sim_pause()
        return self.game_loop.complete_with_results(debriefing)

    def on_simulation_complete(self) -> None:
        logging.debug("Simulation complete")
        self._sim_update_thread.on_sim_pause()
        self.simulation_complete.emit()
