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
    from ..flight import Flight
    from ..flightwaypoint import FlightWaypoint


class Builder(IBuilder):
    def build(self) -> AirliftLayout:
        cargo = self.flight.cargo
        if cargo is None:
            raise PlanningError(
                "Cannot plan transport mission for flight with no cargo."
            )

        altitude = feet(1500)
        altitude_is_agl = True

        builder = WaypointBuilder(self.flight, self.coalition)

        pickup = None
        stopover = None
        if self.flight.is_helo:
            # Create a pickupzone where the cargo will be spawned
            pickup_zone = MissionTarget(
                "Pickup Zone", cargo.origin.position.random_point_within(1000, 200)
            )
            pickup = builder.pickup(pickup_zone)
            # If The cargo is at the departure controlpoint, the pickup waypoint should
            # only be created for client flights
            pickup.only_for_player = cargo.origin == self.flight.departure

            # Create a dropoff zone where the cargo should be dropped
            drop_off_zone = MissionTarget(
                "Dropoff zone",
                cargo.next_stop.position.random_point_within(1000, 200),
            )
            drop_off = builder.drop_off(drop_off_zone)

            # Add an additional stopover point so that the flight can refuel
            stopover = builder.stopover(cargo.next_stop)
        else:
            # Fixed Wing will get stopover points for pickup and dropoff
            if cargo.origin != self.flight.departure:
                pickup = builder.stopover(cargo.origin, "PICKUP")
            drop_off = builder.stopover(cargo.next_stop, "DROP OFF")

        nav_to_pickup = builder.nav_path(
            self.flight.departure.position,
            cargo.origin.position,
            altitude,
            altitude_is_agl,
        )

        if self.flight.client_count > 0:
            # Normal Landing Waypoint
            arrival = builder.land(self.flight.arrival)
        else:
            # The AI Needs another Stopover point to actually fly back to the original
            # base. Otherwise the Cargo drop will be the new Landing Waypoint and the
            # AI will end its mission there instead of flying back.
            # https://forum.dcs.world/topic/211775-landing-to-refuel-and-rearm-the-landingrefuar-waypoint/
            arrival = builder.stopover(self.flight.arrival, "LANDING")

        return AirliftLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to_pickup=nav_to_pickup,
            pickup=pickup,
            nav_to_drop_off=builder.nav_path(
                cargo.origin.position,
                cargo.next_stop.position,
                altitude,
                altitude_is_agl,
            ),
            drop_off=drop_off,
            stopover=stopover,
            nav_to_home=builder.nav_path(
                cargo.origin.position,
                self.flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            arrival=arrival,
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )


@dataclass(frozen=True)
class AirliftLayout(StandardLayout):
    nav_to_pickup: list[FlightWaypoint]
    pickup: FlightWaypoint | None
    nav_to_drop_off: list[FlightWaypoint]
    drop_off: FlightWaypoint
    stopover: FlightWaypoint | None
    nav_to_home: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to_pickup
        if self.pickup is not None:
            yield self.pickup
        yield from self.nav_to_drop_off
        yield self.drop_off
        if self.stopover is not None:
            yield self.stopover
        yield from self.nav_to_home
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class AirliftFlightPlan(StandardFlightPlan[AirliftLayout]):
    def __init__(self, flight: Flight, layout: AirliftLayout) -> None:
        super().__init__(flight, layout)

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def tot_waypoint(self) -> FlightWaypoint | None:
        return self.layout.drop_off

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        # TOT planning isn't really useful for transports. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target
