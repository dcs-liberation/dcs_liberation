from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TYPE_CHECKING, TypeVar

from .flightplan import FlightPlan, Layout

if TYPE_CHECKING:
    from game.coalition import Coalition
    from game.data.doctrine import Doctrine
    from game.theater import ConflictTheater
    from game.threatzones import ThreatZones
    from ..flight import Flight
    from ..package import Package


FlightPlanT = TypeVar("FlightPlanT", bound=FlightPlan[Any])
LayoutT = TypeVar("LayoutT", bound=Layout)


class IBuilder(ABC, Generic[FlightPlanT, LayoutT]):
    def __init__(self, flight: Flight, theater: ConflictTheater) -> None:
        self.flight = flight
        self.theater = theater

    @abstractmethod
    def layout(self) -> LayoutT:
        ...

    @abstractmethod
    def build(self) -> FlightPlanT:
        ...

    @property
    def package(self) -> Package:
        return self.flight.package

    @property
    def coalition(self) -> Coalition:
        return self.flight.coalition

    @property
    def is_player(self) -> bool:
        return self.coalition.player

    @property
    def doctrine(self) -> Doctrine:
        return self.coalition.doctrine

    @property
    def threat_zones(self) -> ThreatZones:
        return self.coalition.opponent.threat_zone
