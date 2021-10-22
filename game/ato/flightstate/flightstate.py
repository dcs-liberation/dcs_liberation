from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from game.ato.starttype import StartType

if TYPE_CHECKING:
    from game.ato.flight import Flight
    from game.settings import Settings


class FlightState(ABC):
    def __init__(self, flight: Flight, settings: Settings) -> None:
        self.flight = flight
        self.settings = settings

    @abstractmethod
    def on_game_tick(self, time: datetime, duration: timedelta) -> None:
        ...

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
