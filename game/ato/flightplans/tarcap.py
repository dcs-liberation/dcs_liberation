from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Type

from game.flightplan.waypointactions.hold import Hold
from game.utils import Distance, Speed, feet
from .capbuilder import CapBuilder
from .patrolling import PatrollingFlightPlan, PatrollingLayout
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class TarCapLayout(PatrollingLayout):
    pre_refuel: FlightWaypoint | None
    nav_from_pre_refuel: list[FlightWaypoint]
    refuel: FlightWaypoint | None

    def __setstate__(self, state: dict[str, object]) -> None:
        state.setdefault("pre_refuel", None)
        state.setdefault("nav_from_pre_refuel", [])
        self.__dict__.update(state)

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield from self.nav_to
        if self.pre_refuel is not None:
            yield self.pre_refuel
            yield from self.nav_from_pre_refuel
        yield self.patrol_start
        yield self.patrol_end
        if self.refuel is not None:
            yield self.refuel
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class TarCapFlightPlan(PatrollingFlightPlan[TarCapLayout]):
    @property
    def patrol_duration(self) -> timedelta:
        # Note that this duration only has an effect if there are no
        # flights in the package that have requested escort. If the package
        # requests an escort the CAP self.flight will remain on station for the
        # duration of the escorted mission, or until it is winchester/bingo.
        return self.flight.coalition.doctrine.cap.duration

    @property
    def patrol_speed(self) -> Speed:
        return self.flight.unit_type.preferred_patrol_speed(
            self.layout.patrol_start.alt
        )

    @property
    def engagement_distance(self) -> Distance:
        return self.flight.coalition.doctrine.cap.engagement_range

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.layout.patrol_start, self.layout.patrol_end}

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=2)

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.pre_refuel:
            return self.pre_refuel_push_time
        if waypoint == self.layout.patrol_end:
            return self.patrol_end_time
        return super().depart_time_for_waypoint(waypoint)

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.pre_refuel:
            return self.pre_refuel_arrival_time
        return super().tot_for_waypoint(waypoint)

    @property
    def pre_refuel_duration(self) -> timedelta:
        if self.layout.pre_refuel is None:
            return timedelta()
        return self.flight.coalition.game.settings.pre_mission_aar_hold_duration

    @property
    def pre_refuel_push_time(self) -> datetime | None:
        if self.layout.pre_refuel is None:
            return None
        return self.patrol_start_time - self._travel_time_after_departure(
            self.layout.pre_refuel, self.layout.patrol_start
        )

    @property
    def pre_refuel_arrival_time(self) -> datetime | None:
        if self.layout.pre_refuel is None:
            return None
        push_time = self.pre_refuel_push_time
        if push_time is None:
            return None
        return push_time - self.pre_refuel_duration

    def total_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        travel_time = super().total_time_between_waypoints(a, b)
        if a != self.layout.pre_refuel:
            return travel_time
        return travel_time + self.pre_refuel_duration

    @property
    def patrol_start_time(self) -> datetime:
        start = self.package.escort_start_time
        if start is not None:
            return start + self.tot_offset
        return self.tot

    @property
    def patrol_end_time(self) -> datetime:
        end = self.package.escort_end_time
        if end is not None:
            return end
        return super().patrol_end_time

    def add_waypoint_actions(self) -> None:
        super().add_waypoint_actions()
        if self.layout.pre_refuel is None:
            return
        pre_refuel = self.layout.pre_refuel
        speed = self.flight.unit_type.patrol_speed
        if speed is None:
            speed = Speed.from_mach(0.6, pre_refuel.alt)
        pre_refuel.add_action(
            Hold(self.pre_refuel_push_time_provider, pre_refuel.alt, speed)
        )

    def pre_refuel_push_time_provider(self) -> datetime:
        push_time = self.pre_refuel_push_time
        assert push_time is not None
        return push_time


class Builder(CapBuilder[TarCapFlightPlan, TarCapLayout]):
    def layout(self) -> TarCapLayout:
        location = self.package.target

        preferred_alt = self.flight.unit_type.preferred_patrol_altitude
        randomized_alt = preferred_alt + feet(random.randint(-2, 1) * 1000)
        patrol_alt = max(
            self.doctrine.cap.min_patrol_altitude,
            min(self.doctrine.cap.max_patrol_altitude, randomized_alt),
        )

        builder = WaypointBuilder(self.flight, self.coalition)
        orbit0p, orbit1p = self.cap_racetrack_for_objective(location, barcap=False)

        start, end = builder.race_track(orbit0p, orbit1p, patrol_alt)

        pre_refuel = None
        nav_to_destination = orbit0p
        nav_from_pre_refuel: list[FlightWaypoint] = []
        refuel = None
        nav_from_origin = orbit1p

        if self.package.waypoints is not None:
            if self.flight.pre_mission_aar:
                pre_refuel = builder.pre_mission_aar(self.package.waypoints.refuel)
                nav_to_destination = pre_refuel.position
                nav_from_pre_refuel = builder.nav_path(
                    pre_refuel.position,
                    orbit0p,
                    patrol_alt,
                )
            refuel = builder.refuel(self.package.waypoints.refuel)
            nav_from_origin = refuel.position

        return TarCapLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, nav_to_destination, patrol_alt
            ),
            nav_from=builder.nav_path(
                nav_from_origin, self.flight.arrival.position, patrol_alt
            ),
            patrol_start=start,
            patrol_end=end,
            pre_refuel=pre_refuel,
            nav_from_pre_refuel=nav_from_pre_refuel,
            refuel=refuel,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self, dump_debug_info: bool = False) -> TarCapFlightPlan:
        return TarCapFlightPlan(self.flight, self.layout())
