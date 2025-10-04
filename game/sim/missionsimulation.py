from __future__ import annotations
import copy
import json
from datetime import timedelta
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.debriefing import Debriefing
from game.missiongenerator import MissionGenerator
from game.settings.settings import FastForwardStopCondition, CombatResolutionMethod
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
        self.time = self.game.simulation_time

    def begin_simulation(self) -> None:
        self.time = self.game.simulation_time
        self.aircraft_simulation.begin_simulation()

    def tick(
        self,
        events: GameUpdateEvents,
        combat_resolution_method: CombatResolutionMethod,
        force_continue: bool,
    ) -> GameUpdateEvents:
        self.time += TICK
        self.game.simulation_time = self.time
        if self.completed:
            raise RuntimeError("Simulation already completed")
        if (
            self.game.settings.fast_forward_stop_condition
            == FastForwardStopCondition.DISABLED
        ):
            events.complete_simulation()
            return events
        self.aircraft_simulation.on_game_tick(
            events, self.time, TICK, combat_resolution_method, force_continue
        )
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

        self.game.save_last_turn_state()
        MissionResultsProcessor(self.game).commit(debriefing, events)
        if self.game.settings.turnless_mode:
            # Set completed to False to clear completion of any previous simulation tick.
            self.completed = False
            # If running in turnless mode, run sim to calculate planned positions of flights
            # for the duration of time the DCS mission ran.
            start_time = copy.deepcopy(self.time)
            while self.time < start_time + timedelta(
                seconds=int(debriefing.state_data.simulation_time_seconds)
            ):
                # Always skip combat as we are processing results from DCS. Any combat has already
                # been resolved in-game
                self.tick(events, CombatResolutionMethod.SKIP, force_continue=True)

    def finish(self) -> None:
        self.unit_map = None
