from __future__ import annotations

from dataclasses import dataclass

from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.data.doctrine import Doctrine
from game.theater.theatergroundobject import NavalGroundObject
from gen.flights.flight import FlightType


@dataclass
class PlanAntiShip(PackagePlanningTask[NavalGroundObject]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.threatening_air_defenses:
            return False
        if not self.target_area_preconditions_met(state, ignore_iads=True):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.eliminate_ship(self.target)

    def propose_flights(self, doctrine: Doctrine) -> None:
        self.propose_flight(FlightType.ANTISHIP, 2, doctrine.mission_ranges.offensive)
        self.propose_flight(
            FlightType.ESCORT,
            2,
            doctrine.mission_ranges.offensive,
            EscortType.AirToAir,
        )
