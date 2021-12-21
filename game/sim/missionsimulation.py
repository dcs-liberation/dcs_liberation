from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.debriefing import Debriefing
from game.missiongenerator import MissionGenerator
from game.unitmap import UnitMap
from .aircraftsimulation import AircraftSimulation
from .gameupdatecallbacks import GameUpdateCallbacks
from .missionresultsprocessor import MissionResultsProcessor

if TYPE_CHECKING:
    from game import Game


TICK = timedelta(seconds=1)


class SimulationAlreadyCompletedError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Simulation already completed")


class MissionSimulation:
    def __init__(self, game: Game, callbacks: GameUpdateCallbacks) -> None:
        self.game = game
        self.unit_map: Optional[UnitMap] = None
        self.aircraft_simulation = AircraftSimulation(self.game, callbacks)
        self.completed = False
        self.time = self.game.conditions.start_time

    def begin_simulation(self) -> None:
        self.time = self.game.conditions.start_time
        self.aircraft_simulation.begin_simulation()

    def tick(self) -> bool:
        self.time += TICK
        if self.completed:
            raise RuntimeError("Simulation already completed")
        self.completed = self.aircraft_simulation.on_game_tick(self.time, TICK)
        return self.completed

    def generate_miz(self, output: Path) -> None:
        self.unit_map = MissionGenerator(self.game, self.time).generate_miz(output)

    def debrief_current_state(
        self, state_path: Path, force_end: bool = False
    ) -> Debriefing:
        if self.unit_map is None:
            raise RuntimeError(
                "Simulation has no unit map. Results processing began before a mission "
                "was generated."
            )

        with state_path.open("r", encoding="utf-8") as state_file:
            data = json.load(state_file)
        if force_end:
            data["mission_ended"] = True
        return Debriefing(data, self.game, self.unit_map)

    def process_results(self, debriefing: Debriefing) -> None:
        if self.unit_map is None:
            raise RuntimeError(
                "Simulation has no unit map. Results processing began before a mission "
                "was generated."
            )

        MissionResultsProcessor(self.game).commit(debriefing)

    def finish(self) -> None:
        self.unit_map = None
