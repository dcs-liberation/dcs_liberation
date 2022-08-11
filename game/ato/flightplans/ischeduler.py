from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from game.ato import Flight
from game.ato.flightplans.flightplan import FlightPlan, Layout

LayoutT = TypeVar("LayoutT", bound=Layout)


class IScheduler(ABC, Generic[LayoutT]):
    def __init__(self, flight: Flight, layout: LayoutT) -> None:
        self.flight = flight
        self.layout = layout

    @abstractmethod
    def schedule(self) -> FlightPlan[LayoutT]:
        ...
