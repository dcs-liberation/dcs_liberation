from __future__ import annotations

from abc import ABC
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING, TypeVar

from dcs import Point

from game.flightplan import HoldZoneGeometry
from game.theater import MissionTarget
from game.utils import Speed, meters
from .flightplan import FlightPlan
from .formation import FormationFlightPlan, FormationLayout
from .ibuilder import IBuilder
from .planningerror import PlanningError
from .waypointbuilder import StrikeTarget, WaypointBuilder
from .. import FlightType
from ..flightwaypoint import FlightWaypoint
from ..flightwaypointtype import FlightWaypointType

if TYPE_CHECKING:
    from ..flight import Flight


class FormationAttackFlightPlan(FormationFlightPlan, ABC):
    @property
    def lead_time(self) -> timedelta:
        return timedelta()

    @property
    def package_speed_waypoints(self) -> set[FlightWaypoint]:
        return {
            self.layout.ingress,
            self.layout.split,
        } | set(self.layout.targets)

    def speed_between_waypoints(self, a: FlightWaypoint, b: FlightWaypoint) -> Speed:
        # FlightWaypoint is only comparable by identity, so adding
        # target_area_waypoint to package_speed_waypoints is useless.
        if b.waypoint_type == FlightWaypointType.TARGET_GROUP_LOC:
            # Should be impossible, as any package with at least one
            # FormationFlightPlan flight needs a formation speed.
            assert self.package.formation_speed is not None
            return self.package.formation_speed
        return super().speed_between_waypoints(a, b)

    @property
    def tot_waypoint(self) -> FlightWaypoint:
        return self.layout.targets[0]

    @property
    def tot_offset(self) -> timedelta:
        try:
            return -self.lead_time
        except AttributeError:
            return timedelta()

    @property
    def target_area_waypoint(self) -> FlightWaypoint:
        return FlightWaypoint(
            "TARGET AREA",
            FlightWaypointType.TARGET_GROUP_LOC,
            self.package.target.position,
            meters(0),
            "RADIO",
        )

    @property
    def travel_time_to_target(self) -> timedelta:
        """The estimated time between the first waypoint and the target."""
        destination = self.tot_waypoint
        total = timedelta()
        for previous_waypoint, waypoint in self.edges():
            if waypoint == self.tot_waypoint:
                # For anything strike-like the TOT waypoint is the *flight's*
                # mission target, but to synchronize with the rest of the
                # package we need to use the travel time to the same position as
                # the others.
                total += self.travel_time_between_waypoints(
                    previous_waypoint, self.target_area_waypoint
                )
                break
            total += self.travel_time_between_waypoints(previous_waypoint, waypoint)
        else:
            raise PlanningError(
                f"Did not find destination waypoint {destination} in "
                f"waypoints for {self.flight}"
            )
        return total

    @property
    def join_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.layout.join, self.layout.ingress
        )
        return self.ingress_time - travel_time

    @property
    def split_time(self) -> timedelta:
        travel_time_ingress = self.travel_time_between_waypoints(
            self.layout.ingress, self.target_area_waypoint
        )
        travel_time_egress = self.travel_time_between_waypoints(
            self.target_area_waypoint, self.layout.split
        )
        minutes_at_target = 0.75 * len(self.layout.targets)
        timedelta_at_target = timedelta(minutes=minutes_at_target)
        return (
            self.ingress_time
            + travel_time_ingress
            + timedelta_at_target
            + travel_time_egress
        )

    @property
    def ingress_time(self) -> timedelta:
        tot = self.tot
        travel_time = self.travel_time_between_waypoints(
            self.layout.ingress, self.target_area_waypoint
        )
        return tot - travel_time

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> timedelta | None:
        if waypoint == self.layout.ingress:
            return self.ingress_time
        elif waypoint in self.layout.targets:
            return self.tot
        return super().tot_for_waypoint(waypoint)


@dataclass(frozen=True)
class FormationAttackLayout(FormationLayout):
    ingress: FlightWaypoint
    targets: list[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.departure
        yield self.hold
        yield from self.nav_to
        yield self.join
        yield self.ingress
        yield from self.targets
        yield self.split
        if self.refuel is not None:
            yield self.refuel
        yield from self.nav_from
        yield self.arrival
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


FlightPlanT = TypeVar("FlightPlanT", bound=FlightPlan[FormationAttackLayout])
LayoutT = TypeVar("LayoutT", bound=FormationAttackLayout)


class FormationAttackBuilder(IBuilder[FlightPlanT, LayoutT], ABC):
    def _build(
        self,
        ingress_type: FlightWaypointType,
        targets: list[StrikeTarget] | None = None,
    ) -> FormationAttackLayout:
        assert self.package.waypoints is not None
        builder = WaypointBuilder(self.flight, self.coalition, targets)

        target_waypoints: list[FlightWaypoint] = []
        if targets is not None:
            for target in targets:
                target_waypoints.append(
                    self.target_waypoint(self.flight, builder, target)
                )
        else:
            target_waypoints.append(
                self.target_area_waypoint(
                    self.flight, self.flight.package.target, builder
                )
            )

        hold = builder.hold(self._hold_point())
        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)
        refuel = builder.refuel(self.package.waypoints.refuel)

        return FormationAttackLayout(
            departure=builder.takeoff(self.flight.departure),
            hold=hold,
            nav_to=builder.nav_path(
                hold.position, join.position, self.doctrine.ingress_altitude
            ),
            join=join,
            ingress=builder.ingress(
                ingress_type, self.package.waypoints.ingress, self.package.target
            ),
            targets=target_waypoints,
            split=split,
            refuel=refuel,
            nav_from=builder.nav_path(
                refuel.position,
                self.flight.arrival.position,
                self.doctrine.ingress_altitude,
            ),
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    @staticmethod
    def target_waypoint(
        flight: Flight, builder: WaypointBuilder, target: StrikeTarget
    ) -> FlightWaypoint:
        if flight.flight_type in {FlightType.ANTISHIP, FlightType.BAI}:
            return builder.bai_group(target)
        elif flight.flight_type == FlightType.DEAD:
            return builder.dead_point(target)
        elif flight.flight_type == FlightType.SEAD:
            return builder.sead_point(target)
        else:
            return builder.strike_point(target)

    @staticmethod
    def target_area_waypoint(
        flight: Flight, location: MissionTarget, builder: WaypointBuilder
    ) -> FlightWaypoint:
        if flight.flight_type == FlightType.DEAD:
            return builder.dead_area(location)
        elif flight.flight_type == FlightType.SEAD:
            return builder.sead_area(location)
        elif flight.flight_type == FlightType.OCA_AIRCRAFT:
            return builder.oca_strike_area(location)
        else:
            return builder.strike_area(location)

    def _hold_point(self) -> Point:
        assert self.package.waypoints is not None
        origin = self.flight.departure.position
        target = self.package.target.position
        join = self.package.waypoints.join
        ip = self.package.waypoints.ingress
        return HoldZoneGeometry(
            target, origin, ip, join, self.coalition, self.theater
        ).find_best_hold_point()
