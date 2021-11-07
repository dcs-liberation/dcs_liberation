from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from dcs import Point

from game.utils import Distance, Speed
from .inflight import InFlight
from ..starttype import StartType

if TYPE_CHECKING:
    from game.sim.aircraftengagementzones import AircraftEngagementZones


class InCombat(InFlight):
    def __init__(self, previous_state: InFlight, description: str) -> None:
        super().__init__(
            previous_state.flight,
            previous_state.settings,
            previous_state.waypoint_index,
        )
        self.previous_state = previous_state
        self._description = description

    def estimate_position(self) -> Point:
        return self.previous_state.estimate_position()

    def estimate_altitude(self) -> tuple[Distance, str]:
        return self.previous_state.estimate_altitude()

    def estimate_speed(self) -> Speed:
        return self.previous_state.estimate_speed()

    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        raise RuntimeError("Cannot simulate combat")

    @property
    def is_waiting_for_start(self) -> bool:
        return False

    def should_halt_sim(self) -> bool:
        return True

    def check_for_combat(
        self, enemy_aircraft_coverage: AircraftEngagementZones
    ) -> None:
        pass

    @property
    def spawn_type(self) -> StartType:
        return StartType.IN_FLIGHT

    @property
    def description(self) -> str:
        return self._description
