from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterator, TYPE_CHECKING, Type

from dcs import Point
from dcs.task import Targets

from game.flightplan import HoldZoneGeometry
from game.flightplan.waypointactions.engagetargets import EngageTargets
from game.flightplan.waypointactions.hold import Hold
from game.flightplan.waypointoptions.formation import Formation
from game.utils import Heading, Speed, nautical_miles
from .ibuilder import IBuilder
from .loiter import LoiterFlightPlan, LoiterLayout
from .waypointbuilder import WaypointBuilder

if TYPE_CHECKING:
    from ..flightwaypoint import FlightWaypoint


@dataclass(frozen=True)
class SweepLayout(LoiterLayout):
    nav_to: list[FlightWaypoint]
    pre_refuel: FlightWaypoint | None
    nav_from_pre_refuel: list[FlightWaypoint]
    sweep_start: FlightWaypoint
    sweep_end: FlightWaypoint
    nav_from: list[FlightWaypoint]

    def __setstate__(self, state: dict[str, object]) -> None:
        state.setdefault("pre_refuel", None)
        state.setdefault("nav_from_pre_refuel", [])
        self.__dict__.update(state)

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield self.hold
        yield from self.nav_to
        if self.pre_refuel is not None:
            yield self.pre_refuel
            yield from self.nav_from_pre_refuel
        yield self.sweep_start
        yield self.sweep_end
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class SweepFlightPlan(LoiterFlightPlan[SweepLayout]):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.layout.sweep_end}

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.sweep_end

    def default_tot_offset(self) -> timedelta:
        return -timedelta(minutes=5)

    @property
    def sweep_start_time(self) -> datetime:
        travel_time = self.total_time_between_waypoints(
            self.layout.sweep_start, self.layout.sweep_end
        )
        return self.sweep_end_time - travel_time

    @property
    def sweep_end_time(self) -> datetime:
        return self.tot

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.pre_refuel:
            return self.pre_refuel_arrival_time
        if waypoint == self.layout.sweep_start:
            return self.sweep_start_time
        if waypoint == self.layout.sweep_end:
            return self.sweep_end_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> datetime | None:
        if waypoint == self.layout.hold:
            return self.push_time
        if waypoint == self.layout.pre_refuel:
            return self.pre_refuel_push_time
        return None

    @property
    def push_time(self) -> datetime:
        return self.sweep_start_time - self._travel_time_after_departure(
            self.layout.hold, self.layout.sweep_start
        )

    @property
    def pre_refuel_duration(self) -> timedelta:
        if self.layout.pre_refuel is None:
            return timedelta()
        return self.flight.coalition.game.settings.pre_mission_aar_hold_duration

    @property
    def pre_refuel_push_time(self) -> datetime | None:
        if self.layout.pre_refuel is None:
            return None
        return self.sweep_start_time - self._travel_time_after_departure(
            self.layout.pre_refuel, self.layout.sweep_start
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
    def mission_begin_on_station_time(self) -> datetime | None:
        return None

    @property
    def mission_departure_time(self) -> datetime:
        return self.sweep_end_time

    def add_waypoint_actions(self) -> None:
        super().add_waypoint_actions()
        if self.layout.pre_refuel is not None:
            pre_refuel = self.layout.pre_refuel
            speed = self.flight.unit_type.patrol_speed
            if speed is None:
                speed = Speed.from_mach(0.6, pre_refuel.alt)
            pre_refuel.add_action(
                Hold(self.pre_refuel_push_time_provider, pre_refuel.alt, speed)
            )
        self.layout.sweep_start.set_option(Formation.LINE_ABREAST_OPEN)
        self.layout.sweep_start.add_action(
            EngageTargets(
                nautical_miles(50),
                [
                    Targets.All.Air.Planes.Fighters,
                    Targets.All.Air.Planes.MultiroleFighters,
                ],
            )
        )

    def pre_refuel_push_time_provider(self) -> datetime:
        push_time = self.pre_refuel_push_time
        assert push_time is not None
        return push_time


class Builder(IBuilder[SweepFlightPlan, SweepLayout]):
    def layout(self) -> SweepLayout:
        assert self.package.waypoints is not None
        target = self.package.target.position
        heading = Heading.from_degrees(
            self.package.waypoints.join.heading_between_point(target)
        )
        start_pos = target.point_from_heading(
            heading.degrees, -self.doctrine.sweep.distance.meters
        )

        builder = WaypointBuilder(self.flight, self.coalition)
        start, end = builder.sweep(start_pos, target, self.doctrine.combat_altitude)

        hold = builder.hold(self._hold_point())
        nav_to = builder.nav_path(
            hold.position, start.position, self.doctrine.combat_altitude
        )
        pre_refuel = None
        nav_from_pre_refuel: list[FlightWaypoint] = []
        if self.flight.pre_mission_aar:
            pre_refuel = builder.pre_mission_aar(self.package.waypoints.refuel)
            nav_to = builder.nav_path(
                hold.position,
                pre_refuel.position,
                self.doctrine.combat_altitude,
            )
            nav_from_pre_refuel = builder.nav_path(
                pre_refuel.position,
                start.position,
                self.doctrine.combat_altitude,
            )

        return SweepLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            nav_to=nav_to,
            pre_refuel=pre_refuel,
            nav_from_pre_refuel=nav_from_pre_refuel,
            nav_from=builder.nav_path(
                end.position,
                self.flight.arrival.position,
                self.doctrine.combat_altitude,
            ),
            sweep_start=start,
            sweep_end=end,
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def _hold_point(self) -> Point:
        assert self.package.waypoints is not None
        origin = self.flight.departure.position
        target = self.package.target.position
        join = self.package.waypoints.join
        ip = self.package.waypoints.ingress
        return HoldZoneGeometry(
            target, origin, ip, join, self.coalition, self.theater
        ).find_best_hold_point()

    def build(self, dump_debug_info: bool = False) -> SweepFlightPlan:
        return SweepFlightPlan(self.flight, self.layout())
