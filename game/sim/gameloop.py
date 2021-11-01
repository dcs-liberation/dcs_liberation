from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, TYPE_CHECKING

from .gamelooptimer import GameLoopTimer
from .missionsimulation import MissionSimulation, SimulationAlreadyCompletedError
from .simspeedsetting import SimSpeedSetting

if TYPE_CHECKING:
    from game import Game
    from game.debriefing import Debriefing


class GameLoop:
    def __init__(self, game: Game, on_complete: Callable[[], None]) -> None:
        self.game = game
        self.on_complete = on_complete
        self.timer = GameLoopTimer(self.tick)
        self.sim = MissionSimulation(self.game)
        self.started = False
        self.completed = False

    def start(self) -> None:
        if self.started:
            raise RuntimeError("Cannot start game loop because it has already started")
        self.started = True
        self.sim.begin_simulation()

    def pause(self) -> None:
        self.set_simulation_speed(SimSpeedSetting.PAUSED)

    def set_simulation_speed(self, simulation_speed: SimSpeedSetting) -> None:
        self.timer.stop()
        if simulation_speed != self.timer.simulation_speed:
            logging.info(f"Speed changed to {simulation_speed}")
        if not self.started:
            self.start()
        self.timer.set_speed(simulation_speed)

    def run_to_first_contact(self) -> None:
        self.pause()
        logging.info("Running sim to first contact")
        while not self.completed:
            self.tick()

    def pause_and_generate_miz(self, output: Path) -> None:
        self.pause()
        self.sim.generate_miz(output)

    def pause_and_debrief(self, state_path: Path, force_end: bool) -> Debriefing:
        self.pause()
        return self.sim.debrief_current_state(state_path, force_end)

    def complete_with_results(self, debriefing: Debriefing) -> None:
        self.pause()
        self.sim.process_results(debriefing)
        self.completed = True

    def tick(self) -> None:
        if not self.started:
            raise RuntimeError("Attempted to tick game loop before initialization")
        try:
            self.completed = self.sim.tick()
            if self.completed:
                self.pause()
                logging.info(f"Simulation completed at {self.sim.time}")
                self.on_complete()
            else:
                logging.info(f"Simulation continued at {self.sim.time}")
        except SimulationAlreadyCompletedError:
            logging.exception("Attempted to tick already completed sim")
