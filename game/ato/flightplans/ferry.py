from __future__ import annotations

from collections.abc import Iterator
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.utils import feet
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .standard import StandardFlightPlan
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(IBuilder):
    def build(self) -> FerryFlightPlan:
        if self.flight.departure == self.flight.arrival:
            raise PlanningError(
                f"Cannot plan ferry self.flight: departure and arrival are both "
                f"{self.flight.departure}"
            )

        altitude_is_agl = self.flight.unit_type.dcs_unit_type.helicopter
        altitude = (
            feet(1500)
            if altitude_is_agl
            else self.flight.unit_type.preferred_patrol_altitude
        )

        builder = WaypointBuilder(self.flight, self.coalition)
        return FerryFlightPlan(
            flight=self.flight,
            departure=builder.takeoff(self.flight.departure),
            nav_to_destination=builder.nav_path(
                self.flight.departure.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )


class FerryFlightPlan(StandardFlightPlan):
    def __init__(
        self,
        flight: Flight,
        departure: FlightWaypoint,
        arrival: FlightWaypoint,
        divert: FlightWaypoint | None,
        bullseye: FlightWaypoint,
        nav_to_destination: list[FlightWaypoint],
    ) -> None:
        super().__init__(flight, departure, arrival, divert, bullseye)
        self.nav_to_destination = nav_to_destination

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to_destination
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def tot_waypoint(self) -> FlightWaypoint | None:
        return self.arrival

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        # TOT planning isn't really useful for ferries. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target
