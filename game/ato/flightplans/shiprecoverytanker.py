from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Iterator, Type
from game.ato.flightplans.standard import StandardFlightPlan, StandardLayout
from game.ato.flightplans.ibuilder import IBuilder
from game.ato.flightplans.standard import StandardLayout
from game.ato.flightplans.waypointbuilder import WaypointBuilder
from game.ato.flightwaypoint import FlightWaypoint
from game.utils import feet


@dataclass(frozen=True)
class RecoveryTankerLayout(StandardLayout):
    nav_to: list[FlightWaypoint]
    recovery_ship: FlightWaypoint
    nav_from: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        yield self.recovery_ship
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class RecoveryTankerFlightPlan(StandardFlightPlan[RecoveryTankerLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.recovery_ship

    @property
    def mission_departure_time(self) -> timedelta:
        return timedelta(hours=2)

    @property
    def patrol_start_time(self) -> timedelta:
        assert self.tot_waypoint.tot is not None
        return self.tot_waypoint.tot

    @property
    def patrol_end_time(self) -> timedelta:
        return self.tot + self.mission_departure_time

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.tot_waypoint:
            return self.tot
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.tot_waypoint:
            return self.tot + self.mission_departure_time
        return None


class Builder(IBuilder[RecoveryTankerFlightPlan, RecoveryTankerLayout]):
    def layout(self) -> RecoveryTankerLayout:

        # TODO: Propagate the ship position.
        ship = self.package.target.position

        builder = WaypointBuilder(self.flight, self.coalition)

        recovery = builder.recovery_tanker(ship)

        tanker_type = self.flight.unit_type
        altitude = tanker_type.preferred_patrol_altitude

        return RecoveryTankerLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(self.flight.departure.position, ship, altitude),
            nav_from=builder.nav_path(ship, self.flight.arrival.position, altitude),
            recovery_ship=recovery,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> RecoveryTankerFlightPlan:
        return RecoveryTankerFlightPlan(self.flight, self.layout())
