from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.debriefing import Debriefing
from game.missiongenerator import MissionGenerator
from game.sim.aircraftsimulation import AircraftSimulation
from game.sim.missionresultsprocessor import MissionResultsProcessor
from game.unitmap import UnitMap

if TYPE_CHECKING:
    from game import Game


class MissionSimulation:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.unit_map: Optional[UnitMap] = None
        self.time = game.conditions.start_time

    def run(self) -> None:
        sim = AircraftSimulation(self.game)
        sim.run()
        self.time = sim.time

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
