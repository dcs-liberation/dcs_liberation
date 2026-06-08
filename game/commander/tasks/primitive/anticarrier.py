from __future__ import annotations

from dataclasses import dataclass

from game.commander.missionproposals import EscortType
from game.commander.tasks.packageplanningtask import PackagePlanningTask
from game.commander.theaterstate import TheaterState
from game.theater import ControlPoint
from game.ato.flighttype import FlightType


@dataclass
class PlanAntiCarrier(PackagePlanningTask[ControlPoint]):
    def preconditions_met(self, state: TheaterState) -> bool:
        if self.target not in state.enemy_carriers:
            return False
        if not self.target_area_preconditions_met(state):
            return False
        return super().preconditions_met(state)

    def apply_effects(self, state: TheaterState) -> None:
        state.enemy_carriers.remove(self.target)

    def propose_flights(self) -> None:
        self.propose_flight(FlightType.ANTISHIP, 4)
        self.propose_flight(FlightType.ESCORT, 4, EscortType.AirToAir)
