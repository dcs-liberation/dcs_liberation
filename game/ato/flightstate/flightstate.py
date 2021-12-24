from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

from game.ato.starttype import StartType

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings
    from game.sim.gameupdateevents import GameUpdateEvents
    from game.threatzones import ThreatPoly


class FlightState(ABC):
    def __init__(self, flight: Flight, settings: Settings) -> None:
        self.flight = flight
        self.settings = settings

    @abstractmethod
    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None:
        ...

    @property
    def vulnerable_to_intercept(self) -> bool:
        return False

    @property
    def vulnerable_to_sam(self) -> bool:
        return False

    @property
    def will_join_air_combat(self) -> bool:
        return False

    def should_halt_sim(self) -> bool:
        return False

    @property
    @abstractmethod
    def is_waiting_for_start(self) -> bool:
        ...

    @property
    @abstractmethod
    def spawn_type(self) -> StartType:
        ...

    def a2a_commit_region(self) -> Optional[ThreatPoly]:
        return None

    def estimate_fuel(self) -> float:
        """Returns the estimated remaining fuel **in kilograms**."""
        if (max_takeoff_fuel := self.flight.max_takeoff_fuel()) is not None:
            return max_takeoff_fuel
        return self.flight.unit_type.dcs_unit_type.fuel_max

    @property
    @abstractmethod
    def description(self) -> str:
        """Describes the current flight state."""
        ...
