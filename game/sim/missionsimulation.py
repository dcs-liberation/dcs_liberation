from __future__ import annotations

import json
from datetime import timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game import persistency
from game.debriefing import Debriefing
from game.missiongenerator import MissionGenerator
from game.unitmap import UnitMap
from .aircraftsimulation import AircraftSimulation
from .missionresultsprocessor import MissionResultsProcessor
from ..profiling import logged_duration

if TYPE_CHECKING:
    from game import Game
    from .gameupdateevents import GameUpdateEvents


TICK = timedelta(seconds=1)


class SimulationAlreadyCompletedError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("Simulation already completed")


class MissionSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.unit_map: Optional[UnitMap] = None
        self.aircraft_simulation = AircraftSimulation(self.game)
        self.completed = False
        self.time = self.game.conditions.start_time

    def begin_simulation(self) -> None:
        self.time = self.game.conditions.start_time
        self.aircraft_simulation.begin_simulation()

    def tick(self, events: GameUpdateEvents) -> GameUpdateEvents:
        self.time += TICK
        if self.completed:
            raise RuntimeError("Simulation already completed")
        self.aircraft_simulation.on_game_tick(events, self.time, TICK)
        self.completed = events.simulation_complete
        return events

    def generate_miz(self, output: Path) -> None:
        with logged_duration("Mission generation"):
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
        debriefing = Debriefing(data, self.game, self.unit_map)
        debriefing.merge_simulation_results(self.aircraft_simulation.results)
        return debriefing

    def process_results(self, debriefing: Debriefing, events: GameUpdateEvents) -> None:
        if self.unit_map is None:
            raise RuntimeError(
                "Simulation has no unit map. Results processing began before a mission "
                "was generated."
            )

        persistency.save_last_turn_state(self.game)
        MissionResultsProcessor(self.game).commit(debriefing, events)

    def finish(self) -> None:
        self.unit_map = None
