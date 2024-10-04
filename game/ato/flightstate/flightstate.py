from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, TYPE_CHECKING

from dcs import Point

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
        self.avoid_further_combat = False

    def reinitialize(self, now: datetime) -> None:
        from game.ato.flightstate import WaitingForStart

        if self.flight.flight_plan.startup_time() <= now:
            self._set_active_flight_state(now)
        else:
            self.flight.set_state(WaitingForStart(self.flight, self.settings))

    def _set_active_flight_state(self, now: datetime) -> None:
        from game.ato.flightstate import StartUp
        from game.ato.flightstate import Taxi
        from game.ato.flightstate import Takeoff
        from game.ato.flightstate import Navigating

        match self.flight.start_type:
            case StartType.COLD:
                self.flight.set_state(StartUp(self.flight, self.settings, now))
            case StartType.WARM:
                self.flight.set_state(Taxi(self.flight, self.settings, now))
            case StartType.RUNWAY:
                self.flight.set_state(Takeoff(self.flight, self.settings, now))
            case StartType.IN_FLIGHT:
                self.flight.set_state(
                    Navigating(self.flight, self.settings, waypoint_index=0)
                )
            case _:
                raise ValueError(
                    f"Unknown start type {self.flight.start_type} for {self.flight}"
                )

    @property
    def alive(self) -> bool:
        return True

    @property
    @abstractmethod
    def cancelable(self) -> bool: ...

    @abstractmethod
    def on_game_tick(
        self, events: GameUpdateEvents, time: datetime, duration: timedelta
    ) -> None: ...

    @property
    def in_flight(self) -> bool:
        return False

    @property
    def is_at_ip(self) -> bool:
        return False

    @property
    def in_combat(self) -> bool:
        return False

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
    def is_waiting_for_start(self) -> bool: ...

    @abstractmethod
    def estimate_position(self) -> Point: ...

    @property
    @abstractmethod
    def spawn_type(self) -> StartType: ...

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
