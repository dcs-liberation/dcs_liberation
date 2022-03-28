from __future__ import annotations
from dataclasses import dataclass

from datetime import timedelta
from typing import Iterator, Type
from game.ato.flightplans.patrolling import PatrollingFlightPlan, PatrollingLayout
from game.ato.flightplans.waypointbuilder import StrikeTarget, WaypointBuilder

from game.ato.flightwaypoint import FlightWaypoint
from game.theater.theatergroundobject import TheaterGroundObject
from game.utils import Distance, Speed, knots, meters

from .formationattack import (
    FormationAttackBuilder,
    FormationAttackFlightPlan,
    FormationAttackLayout,
)
from .. import Flight
from ..flightwaypointtype import FlightWaypointType


@dataclass(frozen=True)
class SeadLayout(FormationAttackLayout, PatrollingLayout):
    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield self.hold
        yield from self.nav_to
        yield self.join
        yield self.ingress
        yield self.patrol_start
        yield from self.targets
        yield self.patrol_end
        yield self.split
        if self.refuel is not None:
            yield self.refuel
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


class SeadFlightPlan(FormationAttackFlightPlan, PatrollingFlightPlan[SeadLayout]):
    def __init__(self, flight: Flight, layout: SeadLayout) -> None:
        super().__init__(flight, layout)

    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def lead_time(self) -> timedelta:
        return timedelta(minutes=1)

    @property
    def patrol_duration(self) -> timedelta:
        # Keep the SEAD Flight searching for 3mins
        return timedelta(minutes=3)

    @property
    def patrol_speed(self) -> Speed:
        # TODO Correct speed as they are in alert
        if self.flight.unit_type.patrol_speed is not None:
            return self.flight.unit_type.patrol_speed
        # ~280 knots IAS at 21000.
        return knots(400)

    @property
    def combat_speed_waypoints(self) -> set[FlightWaypoint]:
        return {self.layout.patrol_start, self.layout.patrol_end}

    @property
    def engagement_distance(self) -> Distance:
        if isinstance(self.package.target, TheaterGroundObject):
            return self.package.target.max_threat_range()
        return meters(0)

    def request_escort_at(self) -> FlightWaypoint | None:
        return self.layout.ingress

    def dismiss_escort_at(self) -> FlightWaypoint | None:
        return self.layout.split


class Builder(FormationAttackBuilder):
    def build(self) -> SeadLayout:
        location = self.package.target
        assert self.package.waypoints is not None
        assert isinstance(location, TheaterGroundObject)
        targets = [
            StrikeTarget(f"{group.group_name} at {location.name}", group)
            for group in location.groups
            if group.units
        ]
        builder = WaypointBuilder(self.flight, self.coalition, targets)
        target_waypoints = [
            self.target_waypoint(self.flight, builder, target) for target in targets
        ]

        heading_from_target = location.position.heading_between_point(
            self.package.waypoints.ingress
        )
        distance = location.max_threat_range().meters / 3 * 2
        # 2/3 the range circle along the line from target to ingress
        search_start = location.position.point_from_heading(
            heading_from_target, distance
        )
        # 2/3 the range circle with a 45-90 angle
        search_end = location.position.point_from_heading(
            heading_from_target + 90, distance
        )
        sead_search = builder.race_track(
            search_start, search_end, self.doctrine.ingress_altitude
        )
        sead_search[0].name = "SEAD SEARCH START"
        sead_search[1].name = "SEAD SEARCH END"

        hold = builder.hold(self._hold_point())
        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)
        refuel = None
        if self.package.waypoints.refuel is not None:
            refuel = builder.refuel(self.package.waypoints.refuel)

        return SeadLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            nav_to=builder.nav_path(
                hold.position, join.position, self.doctrine.ingress_altitude
            ),
            join=join,
            ingress=builder.ingress(
                FlightWaypointType.INGRESS_SEAD,
                self.package.waypoints.ingress,
                self.package.target,
            ),
            patrol_start=sead_search[0],
            targets=target_waypoints,
            patrol_end=sead_search[1],
            split=split,
            refuel=refuel,
            nav_from=builder.nav_path(
                split.position,
                self.flight.arrival.position,
                self.doctrine.ingress_altitude,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )
