from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, Type

from game.theater.missiontarget import MissionTarget
from game.utils import feet
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .standard import StandardFlightPlan, StandardLayout
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class AirliftLayout(StandardLayout):
    nav_to_pickup: list[FlightWaypoint]
    # There will not be a pickup waypoint when the pickup airfield is the departure
    # airfield for cargo planes, as the cargo is pre-loaded. Helicopters will still pick
    # up the cargo near the airfield.
    pickup: FlightWaypoint | None
    # pickup_zone will be used for player flights to create the CTLD stuff
    ctld_pickup_zone: FlightWaypoint | None
    nav_to_drop_off: list[FlightWaypoint]
    # There will not be a drop-off waypoint when the drop-off airfield and the arrival
    # airfield is the same for a cargo plane, as planes will land to unload and we don't
    # want a double landing. Helicopters will still drop their cargo near the airfield
    # before landing.
    drop_off: FlightWaypoint | None
    # drop_off_zone will be used for player flights to create the CTLD stuff
    ctld_drop_off_zone: FlightWaypoint | None
    nav_to_home: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to_pickup
        if self.pickup is not None:
            yield self.pickup
        if self.ctld_pickup_zone is not None:
            yield self.ctld_pickup_zone
        yield from self.nav_to_drop_off
        if self.drop_off is not None:
            yield self.drop_off
        if self.ctld_drop_off_zone is not None:
            yield self.ctld_drop_off_zone
        yield from self.nav_to_home
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirliftFlightPlan(StandardFlightPlan[AirliftLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        # The TOT is the time that the cargo will be dropped off. If the drop-off
        # location is the arrival airfield and this is not a helicopter flight, there
        # will not be a separate drop-off waypoint; the arrival landing waypoint is the
        # drop-off waypoint.
        return self.layout.drop_off or self.layout.arrival

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        # TOT planning isn't really useful for transports. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target


class Builder(IBuilder[AirliftFlightPlan, AirliftLayout]):
    def layout(self) -> AirliftLayout:
        cargo = self.flight.cargo
        if cargo is None:
            raise PlanningError(
                "Cannot plan transport mission for flight with no cargo."
            )

        altitude = feet(1500)
        altitude_is_agl = True

        builder = WaypointBuilder(self.flight, self.coalition)

        pickup = None
        drop_off = None
        pickup_zone = None
        drop_off_zone = None

        if cargo.origin != self.flight.departure:
            pickup = builder.cargo_stop(cargo.origin)
        if cargo.next_stop != self.flight.arrival:
            drop_off = builder.cargo_stop(cargo.next_stop)

        if self.flight.is_helo:
            # Create CTLD Zones for Helo flights
            pickup_zone = builder.pickup_zone(
                MissionTarget(
                    "Pickup Zone", cargo.origin.position.random_point_within(1000, 200)
                )
            )
            drop_off_zone = builder.dropoff_zone(
                MissionTarget(
                    "Dropoff zone",
                    cargo.next_stop.position.random_point_within(1000, 200),
                )
            )
            # Show the zone waypoints only to the player
            pickup_zone.only_for_player = True
            drop_off_zone.only_for_player = True

        nav_to_pickup = builder.nav_path(
            self.flight.departure.position,
            cargo.origin.position,
            altitude,
            altitude_is_agl,
        )

        return AirliftLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to_pickup=nav_to_pickup,
            pickup=pickup,
            ctld_pickup_zone=pickup_zone,
            nav_to_drop_off=builder.nav_path(
                cargo.origin.position,
                cargo.next_stop.position,
                altitude,
                altitude_is_agl,
            ),
            drop_off=drop_off,
            ctld_drop_off_zone=drop_off_zone,
            nav_to_home=builder.nav_path(
                cargo.origin.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> AirliftFlightPlan:
        return AirliftFlightPlan(self.flight, self.layout())
