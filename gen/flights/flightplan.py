"""Flight plan generation.

Flights are first planned generically by either the player or by the
MissionPlanner. Those only plan basic information like the objective, aircraft
type, and the size of the flight. The FlightPlanBuilder is responsible for
generating the waypoints for the mission.
"""
from __future__ import annotations

import logging
import math
import random
from dataclasses import dataclass, field
from datetime import timedelta
from functools import cached_property
from typing import Iterator, List, Optional, Set, TYPE_CHECKING, Tuple

from dcs.mapping import Point
from dcs.unit import Unit
from shapely.geometry import Point as ShapelyPoint

from game.data.doctrine import Doctrine
from game.dcs.aircrafttype import FuelConsumption
from game.flightplan import IpZoneGeometry, JoinZoneGeometry, HoldZoneGeometry
from game.theater import (
    Airfield,
    ControlPoint,
    FrontLine,
    MissionTarget,
    SamGroundObject,
    TheaterGroundObject,
    NavalControlPoint,
    ConflictTheater,
)
from game.theater.theatergroundobject import (
    EwrGroundObject,
    NavalGroundObject,
    BuildingGroundObject,
)

from game.threatzones import ThreatZones
from game.utils import Distance, Heading, Speed, feet, meters, nautical_miles, knots

from .closestairfields import ObjectiveDistanceCache
from .flight import Flight, FlightType, FlightWaypoint, FlightWaypointType
from .traveltime import GroundSpeed, TravelTime
from .waypointbuilder import StrikeTarget, WaypointBuilder
from ..conflictgen import Conflict, FRONTLINE_LENGTH

if TYPE_CHECKING:
    from gen.ato import Package
    from game.coalition import Coalition
    from game.transfers import Convoy

INGRESS_TYPES = {
    FlightWaypointType.INGRESS_CAS,
    FlightWaypointType.INGRESS_ESCORT,
    FlightWaypointType.INGRESS_SEAD,
    FlightWaypointType.INGRESS_STRIKE,
    FlightWaypointType.INGRESS_DEAD,
}


class PlanningError(RuntimeError):
    """Raised when the flight planner was unable to create a flight plan."""


class InvalidObjectiveLocation(PlanningError):
    """Raised when the objective location is invalid for the mission type."""

    def __init__(self, task: FlightType, location: MissionTarget) -> None:
        super().__init__(f"{location.name} is not valid for {task} missions.")


@dataclass(frozen=True)
class FlightPlan:
    package: Package
    flight: Flight

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        """A list of all waypoints in the flight plan, in order."""
        return list(self.iter_waypoints())

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        """Iterates over all waypoints in the flight plan, in order."""
        raise NotImplementedError

    def edges(
        self, until: Optional[FlightWaypoint] = None
    ) -> Iterator[Tuple[FlightWaypoint, FlightWaypoint]]:
        """A list of all paths between waypoints, in order."""
        waypoints = self.waypoints
        if until is None:
            last_index = len(waypoints)
        else:
            last_index = waypoints.index(until) + 1

        return zip(self.waypoints[:last_index], self.waypoints[1:last_index])

    def best_speed_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> Speed:
        """Desired ground speed between points a and b."""
        factor = 1.0
        if b.waypoint_type == FlightWaypointType.ASCEND_POINT:
            # Flights that start airborne already have some altitude and a good
            # amount of speed.
            factor = 0.5
        elif b.waypoint_type == FlightWaypointType.LOITER:
            # On the way to the hold point the AI won't climb unless they're in
            # formation, so slowing down the flight lead gives them more time to
            # form up and climb.
            # https://forums.eagle.ru/forum/english/digital-combat-simulator/dcs-world-2-5/dcs-wishlist-aa/7121300-ai-flights-will-not-climb-to-hold-point-because-wingman-not-joined
            #
            # Plus, it's a loiter point so there's no reason to hurry.
            factor = 0.75
        # TODO: Adjust if AGL.
        # We don't have an exact heightmap, but we should probably be performing
        # *some* adjustment for NTTR since the minimum altitude of the map is
        # near 2000 ft MSL.
        return GroundSpeed.for_flight(self.flight, min(a.alt, b.alt)) * factor

    def speed_between_waypoints(self, a: FlightWaypoint, b: FlightWaypoint) -> Speed:
        return self.best_speed_between_waypoints(a, b)

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        """The waypoint that is associated with the package TOT, or None.

        Note that the only flight plans that should have no target waypoints are
        user-planned missions without any useful waypoints and flight plans that
        failed to generate. Nevertheless, we have to defend against it.
        """
        raise NotImplementedError

    @property
    def tot(self) -> timedelta:
        return self.package.time_over_target + self.tot_offset

    @cached_property
    def bingo_fuel(self) -> int:
        """Bingo fuel value for the FlightPlan"""
        if (fuel := self.flight.unit_type.fuel_consumption) is not None:
            return self._bingo_estimate(fuel)
        return self._legacy_bingo_estimate()

    def _bingo_estimate(self, fuel: FuelConsumption) -> int:
        distance_to_arrival = self.max_distance_from(self.flight.arrival)
        fuel_consumed = fuel.cruise * distance_to_arrival.nautical_miles
        bingo = fuel_consumed + fuel.min_safe
        return math.ceil(bingo / 100) * 100

    def _legacy_bingo_estimate(self) -> int:
        distance_to_arrival = self.max_distance_from(self.flight.arrival)

        bingo = 1000.0  # Minimum Emergency Fuel
        bingo += 500  # Visual Traffic
        bingo += 15 * distance_to_arrival.nautical_miles

        # TODO: Per aircraft tweaks.

        if self.flight.divert is not None:
            max_divert_distance = self.max_distance_from(self.flight.divert)
            bingo += 10 * max_divert_distance.nautical_miles

        return round(bingo / 100) * 100

    @cached_property
    def joker_fuel(self) -> int:
        """Joker fuel value for the FlightPlan"""
        return self.bingo_fuel + 1000

    def max_distance_from(self, cp: ControlPoint) -> Distance:
        """Returns the farthest waypoint of the flight plan from a ControlPoint.
        :arg cp The ControlPoint to measure distance from.
        """
        if not self.waypoints:
            return meters(0)
        return max(
            [meters(cp.position.distance_to_point(w.position)) for w in self.waypoints]
        )

    @property
    def tot_offset(self) -> timedelta:
        """This flight's offset from the package's TOT.

        Positive values represent later TOTs. An offset of -2 minutes is used
        for a flight that has a TOT 2 minutes before the rest of the package.
        """
        return timedelta()

    def _travel_time_to_waypoint(self, destination: FlightWaypoint) -> timedelta:
        total = timedelta()

        if destination not in self.waypoints:
            raise PlanningError(
                f"Did not find destination waypoint {destination} in "
                f"waypoints for {self.flight}"
            )

        for previous_waypoint, waypoint in self.edges(until=destination):
            total += self.travel_time_between_waypoints(previous_waypoint, waypoint)
        return total

    def travel_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        return TravelTime.between_points(
            a.position, b.position, self.speed_between_waypoints(a, b)
        )

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        raise NotImplementedError

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        raise NotImplementedError

    def request_escort_at(self) -> Optional[FlightWaypoint]:
        return None

    def dismiss_escort_at(self) -> Optional[FlightWaypoint]:
        return None

    def escorted_waypoints(self) -> Iterator[FlightWaypoint]:
        begin = self.request_escort_at()
        end = self.dismiss_escort_at()
        if begin is None or end is None:
            return
        escorting = False
        for waypoint in self.waypoints:
            if waypoint == begin:
                escorting = True
            if escorting:
                yield waypoint
            if waypoint == end:
                return

    def takeoff_time(self) -> Optional[timedelta]:
        tot_waypoint = self.tot_waypoint
        if tot_waypoint is None:
            return None
        return self.tot - self._travel_time_to_waypoint(tot_waypoint)

    def startup_time(self) -> Optional[timedelta]:
        takeoff_time = self.takeoff_time()
        if takeoff_time is None:
            return None

        start_time = takeoff_time - self.estimate_startup() - self.estimate_ground_ops()

        # In case FP math has given us some barely below zero time, round to
        # zero.
        if math.isclose(start_time.total_seconds(), 0):
            return timedelta()

        # Trim microseconds. DCS doesn't handle sub-second resolution for tasks,
        # and they're not interesting from a mission planning perspective so we
        # don't want them in the UI.
        #
        # Round down so *barely* above zero start times are just zero.
        return timedelta(seconds=math.floor(start_time.total_seconds()))

    def estimate_startup(self) -> timedelta:
        if self.flight.start_type == "Cold":
            if self.flight.client_count:
                return timedelta(minutes=10)
            else:
                # The AI doesn't seem to have a real startup procedure.
                return timedelta(minutes=2)
        return timedelta()

    def estimate_ground_ops(self) -> timedelta:
        if self.flight.start_type in ("Runway", "In Flight"):
            return timedelta()
        if self.flight.from_cp.is_fleet:
            return timedelta(minutes=2)
        else:
            return timedelta(minutes=8)

    @property
    def mission_departure_time(self) -> timedelta:
        """The time that the mission is complete and the flight RTBs."""
        raise NotImplementedError


@dataclass(frozen=True)
class LoiterFlightPlan(FlightPlan):
    hold: FlightWaypoint
    hold_duration: timedelta

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        raise NotImplementedError

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        raise NotImplementedError

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        raise NotImplementedError

    @property
    def push_time(self) -> timedelta:
        raise NotImplementedError

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.hold:
            return self.push_time
        return None

    def travel_time_between_waypoints(
        self, a: FlightWaypoint, b: FlightWaypoint
    ) -> timedelta:
        travel_time = super().travel_time_between_waypoints(a, b)
        if a != self.hold:
            return travel_time
        return travel_time + self.hold_duration

    @property
    def mission_departure_time(self) -> timedelta:
        raise NotImplementedError


@dataclass(frozen=True)
class FormationFlightPlan(LoiterFlightPlan):
    join: FlightWaypoint
    split: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        raise NotImplementedError

    @property
    def package_speed_waypoints(self) -> Set[FlightWaypoint]:
        raise NotImplementedError

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        raise NotImplementedError

    def request_escort_at(self) -> Optional[FlightWaypoint]:
        return self.join

    def dismiss_escort_at(self) -> Optional[FlightWaypoint]:
        return self.split

    @cached_property
    def best_flight_formation_speed(self) -> Speed:
        """The best speed this flight is capable at all formation waypoints.

        To ease coordination with other flights, we aim to have a single mission
        speed used by the formation for all waypoints. As such, this function
        returns the highest ground speed that the flight is capable of flying at
        all of its formation waypoints.
        """
        speeds = []
        for previous_waypoint, waypoint in self.edges():
            if waypoint in self.package_speed_waypoints:
                speeds.append(
                    self.best_speed_between_waypoints(previous_waypoint, waypoint)
                )
        return min(speeds)

    def speed_between_waypoints(self, a: FlightWaypoint, b: FlightWaypoint) -> Speed:
        if b in self.package_speed_waypoints:
            # Should be impossible, as any package with at least one
            # FormationFlightPlan flight needs a formation speed.
            assert self.package.formation_speed is not None
            return self.package.formation_speed
        return super().speed_between_waypoints(a, b)

    @property
    def travel_time_to_rendezvous(self) -> timedelta:
        """The estimated time between the first waypoint and the join point."""
        return self._travel_time_to_waypoint(self.join)

    @property
    def join_time(self) -> timedelta:
        raise NotImplementedError

    @property
    def split_time(self) -> timedelta:
        raise NotImplementedError

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.join:
            return self.join_time
        elif waypoint == self.split:
            return self.split_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.join_time - TravelTime.between_points(
            self.hold.position,
            self.join.position,
            GroundSpeed.for_flight(self.flight, self.hold.alt),
        )

    @property
    def mission_departure_time(self) -> timedelta:
        return self.split_time


@dataclass(frozen=True)
class PatrollingFlightPlan(FlightPlan):
    nav_to: List[FlightWaypoint]
    nav_from: List[FlightWaypoint]
    patrol_start: FlightWaypoint
    patrol_end: FlightWaypoint

    #: Maximum time to remain on station.
    patrol_duration: timedelta

    #: The engagement range of any Search Then Engage task, or the radius of a
    #: Search Then Engage in Zone task. Any enemies of the appropriate type for
    #: this mission within this range of the flight's current position (or the
    #: center of the zone) will be engaged by the flight.
    engagement_distance: Distance

    @property
    def patrol_start_time(self) -> timedelta:
        return self.package.time_over_target

    @property
    def patrol_end_time(self) -> timedelta:
        # TODO: This is currently wrong for CAS.
        # CAS missions end when they're winchester or bingo. We need to
        # configure push tasks for the escorts rather than relying on timing.
        return self.patrol_start_time + self.patrol_duration

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.patrol_start:
            return self.patrol_start_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.patrol_end:
            return self.patrol_end_time
        return None

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        raise NotImplementedError

    @property
    def package_speed_waypoints(self) -> Set[FlightWaypoint]:
        return {self.patrol_start, self.patrol_end}

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        return self.patrol_start

    @property
    def mission_departure_time(self) -> timedelta:
        return self.patrol_end_time


@dataclass(frozen=True)
class BarCapFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield from self.nav_to
        yield from [
            self.patrol_start,
            self.patrol_end,
        ]
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


@dataclass(frozen=True)
class CasFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    target: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield from self.nav_to
        yield from [
            self.patrol_start,
            self.target,
            self.patrol_end,
        ]
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    def request_escort_at(self) -> Optional[FlightWaypoint]:
        return self.patrol_start

    def dismiss_escort_at(self) -> Optional[FlightWaypoint]:
        return self.patrol_end


@dataclass(frozen=True)
class TarCapFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint
    lead_time: timedelta

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield from self.nav_to
        yield from [
            self.patrol_start,
            self.patrol_end,
        ]
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.patrol_end:
            return self.patrol_end_time
        return super().depart_time_for_waypoint(waypoint)

    @property
    def patrol_start_time(self) -> timedelta:
        start = self.package.escort_start_time
        if start is not None:
            return start + self.tot_offset
        return self.tot

    @property
    def patrol_end_time(self) -> timedelta:
        end = self.package.escort_end_time
        if end is not None:
            return end
        return super().patrol_end_time


@dataclass(frozen=True)
class StrikeFlightPlan(FormationFlightPlan):
    takeoff: FlightWaypoint
    hold: FlightWaypoint
    nav_to: List[FlightWaypoint]
    join: FlightWaypoint
    ingress: FlightWaypoint
    targets: List[FlightWaypoint]
    split: FlightWaypoint
    nav_from: List[FlightWaypoint]
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint
    lead_time: timedelta = field(default_factory=timedelta)

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield self.hold
        yield from self.nav_to
        yield self.join
        yield self.ingress
        yield from self.targets
        yield self.split
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def package_speed_waypoints(self) -> Set[FlightWaypoint]:
        return {
            self.ingress,
            self.split,
        } | set(self.targets)

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
        return self.targets[0]

    @property
    def tot_offset(self) -> timedelta:
        try:
            return -self.lead_time
        except AttributeError:
            return timedelta()

    @property
    def target_area_waypoint(self) -> FlightWaypoint:
        return FlightWaypoint(
            FlightWaypointType.TARGET_GROUP_LOC,
            self.package.target.position.x,
            self.package.target.position.y,
            meters(0),
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
        travel_time = self.travel_time_between_waypoints(self.join, self.ingress)
        return self.ingress_time - travel_time

    @property
    def split_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(self.ingress, self.split)
        return self.ingress_time + travel_time

    @property
    def ingress_time(self) -> timedelta:
        tot = self.tot
        travel_time = self.travel_time_between_waypoints(
            self.ingress, self.target_area_waypoint
        )
        return tot - travel_time

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.ingress:
            return self.ingress_time
        elif waypoint in self.targets:
            return self.tot
        return super().tot_for_waypoint(waypoint)


@dataclass(frozen=True)
class SweepFlightPlan(LoiterFlightPlan):
    takeoff: FlightWaypoint
    nav_to: List[FlightWaypoint]
    sweep_start: FlightWaypoint
    sweep_end: FlightWaypoint
    nav_from: List[FlightWaypoint]
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint
    lead_time: timedelta

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield self.hold
        yield from self.nav_to
        yield self.sweep_start
        yield self.sweep_end
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        return self.sweep_end

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    @property
    def sweep_start_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.sweep_start, self.sweep_end
        )
        return self.sweep_end_time - travel_time

    @property
    def sweep_end_time(self) -> timedelta:
        return self.tot

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.sweep_start:
            return self.sweep_start_time
        if waypoint == self.sweep_end:
            return self.sweep_end_time
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.hold:
            return self.push_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.sweep_end_time - TravelTime.between_points(
            self.hold.position,
            self.sweep_end.position,
            GroundSpeed.for_flight(self.flight, self.hold.alt),
        )

    def mission_departure_time(self) -> timedelta:
        return self.sweep_end_time


@dataclass(frozen=True)
class AwacsFlightPlan(LoiterFlightPlan):
    takeoff: FlightWaypoint
    nav_to: List[FlightWaypoint]
    nav_from: List[FlightWaypoint]
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield from self.nav_to
        yield self.hold
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def mission_start_time(self) -> Optional[timedelta]:
        return self.takeoff_time()

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.hold:
            return self.package.time_over_target
        return None

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        return self.hold

    @property
    def push_time(self) -> timedelta:
        return self.package.time_over_target + self.hold_duration

    @property
    def mission_departure_time(self) -> timedelta:
        return self.push_time


@dataclass(frozen=True)
class RefuelingFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint

    #: Racetrack speed.
    patrol_speed: Speed

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield from self.nav_to
        yield self.patrol_start
        yield self.patrol_end
        yield from self.nav_from
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye


@dataclass(frozen=True)
class AirliftFlightPlan(FlightPlan):
    takeoff: FlightWaypoint
    nav_to_pickup: List[FlightWaypoint]
    pickup: Optional[FlightWaypoint]
    nav_to_drop_off: List[FlightWaypoint]
    drop_off: FlightWaypoint
    nav_to_home: List[FlightWaypoint]
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    bullseye: FlightWaypoint

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield self.takeoff
        yield from self.nav_to_pickup
        if self.pickup:
            yield self.pickup
        yield from self.nav_to_drop_off
        yield self.drop_off
        yield from self.nav_to_home
        yield self.land
        if self.divert is not None:
            yield self.divert
        yield self.bullseye

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        return self.drop_off

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        # TOT planning isn't really useful for transports. They're behind the front
        # lines so no need to wait for escorts or for other missions to complete.
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target


@dataclass(frozen=True)
class CustomFlightPlan(FlightPlan):
    custom_waypoints: List[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from self.custom_waypoints

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        target_types = (
            FlightWaypointType.PATROL_TRACK,
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )
        for waypoint in self.waypoints:
            if waypoint in target_types:
                return waypoint
        return None

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.tot_waypoint:
            return self.package.time_over_target
        return None

    def depart_time_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        return None

    @property
    def mission_departure_time(self) -> timedelta:
        return self.package.time_over_target


class FlightPlanBuilder:
    """Generates flight plans for flights."""

    def __init__(
        self, package: Package, coalition: Coalition, theater: ConflictTheater
    ) -> None:
        # TODO: Plan similar altitudes for the in-country leg of the mission.
        # Waypoint altitudes for a given flight *shouldn't* differ too much
        # between the join and split points, so we don't need speeds for each
        # leg individually since they should all be fairly similar. This doesn't
        # hold too well right now since nothing is stopping each waypoint from
        # jumping 20k feet each time, but that's a huge waste of energy we
        # should be avoiding anyway.
        self.package = package
        self.coalition = coalition
        self.theater = theater

    @property
    def is_player(self) -> bool:
        return self.coalition.player

    @property
    def doctrine(self) -> Doctrine:
        return self.coalition.doctrine

    @property
    def threat_zones(self) -> ThreatZones:
        return self.coalition.opponent.threat_zone

    def populate_flight_plan(
        self,
        flight: Flight,
        # TODO: Custom targets should be an attribute of the flight.
        custom_targets: Optional[List[Unit]] = None,
    ) -> None:
        """Creates a default flight plan for the given mission."""
        if flight not in self.package.flights:
            raise RuntimeError("Flight must be a part of the package")

        from game.navmesh import NavMeshError

        try:
            if self.package.waypoints is None:
                self.regenerate_package_waypoints()
            flight.flight_plan = self.generate_flight_plan(flight, custom_targets)
        except NavMeshError as ex:
            color = "blue" if self.is_player else "red"
            raise PlanningError(
                f"Could not plan {color} {flight.flight_type.value} from "
                f"{flight.departure} to {flight.package.target}"
            ) from ex

    def generate_flight_plan(
        self, flight: Flight, custom_targets: Optional[List[Unit]]
    ) -> FlightPlan:
        # TODO: Flesh out mission types.
        task = flight.flight_type
        if task == FlightType.ANTISHIP:
            return self.generate_anti_ship(flight)
        elif task == FlightType.BAI:
            return self.generate_bai(flight)
        elif task == FlightType.BARCAP:
            return self.generate_barcap(flight)
        elif task == FlightType.CAS:
            return self.generate_cas(flight)
        elif task == FlightType.DEAD:
            return self.generate_dead(flight, custom_targets)
        elif task == FlightType.ESCORT:
            return self.generate_escort(flight)
        elif task == FlightType.OCA_AIRCRAFT:
            return self.generate_oca_strike(flight)
        elif task == FlightType.OCA_RUNWAY:
            return self.generate_runway_attack(flight)
        elif task == FlightType.SEAD:
            return self.generate_sead(flight, custom_targets)
        elif task == FlightType.SEAD_ESCORT:
            return self.generate_escort(flight)
        elif task == FlightType.STRIKE:
            return self.generate_strike(flight)
        elif task == FlightType.SWEEP:
            return self.generate_sweep(flight)
        elif task == FlightType.TARCAP:
            return self.generate_tarcap(flight)
        elif task == FlightType.AEWC:
            return self.generate_aewc(flight)
        elif task == FlightType.TRANSPORT:
            return self.generate_transport(flight)
        elif task == FlightType.REFUELING:
            return self.generate_refueling_racetrack(flight)
        raise PlanningError(f"{task} flight plan generation not implemented")

    def regenerate_package_waypoints(self) -> None:
        from gen.ato import PackageWaypoints

        package_airfield = self.package_airfield()

        # Start by picking the best IP for the attack.
        ingress_point = IpZoneGeometry(
            self.package.target.position,
            package_airfield.position,
            self.coalition,
        ).find_best_ip()

        join_point = JoinZoneGeometry(
            self.package.target.position,
            package_airfield.position,
            ingress_point,
            self.coalition,
        ).find_best_join_point()

        # And the split point based on the best route from the IP. Since that's no
        # different than the best route *to* the IP, this is the same as the join point.
        # TODO: Estimate attack completion point based on the IP and split from there?
        self.package.waypoints = PackageWaypoints(
            WaypointBuilder.perturb(join_point),
            ingress_point,
            WaypointBuilder.perturb(join_point),
        )

    def generate_strike(self, flight: Flight) -> StrikeFlightPlan:
        """Generates a strike flight plan.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        # TODO: Support airfield strikes.
        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        targets: List[StrikeTarget] = []
        if isinstance(location, BuildingGroundObject):
            # A building "group" is implemented as multiple TGOs with the same name.
            for building in location.strike_targets:
                targets.append(StrikeTarget(building.category, building))
        else:
            # TODO: Replace with DEAD?
            # Strike missions on SEAD targets target units.
            for g in location.groups:
                for j, u in enumerate(g.units):
                    targets.append(StrikeTarget(f"{u.type} #{j}", u))

        return self.strike_flightplan(
            flight, location, FlightWaypointType.INGRESS_STRIKE, targets
        )

    def generate_aewc(self, flight: Flight) -> AwacsFlightPlan:
        """Generate a AWACS flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        orbit_location = self.aewc_orbit(location)

        if flight.unit_type.patrol_altitude is not None:
            patrol_alt = flight.unit_type.patrol_altitude
        else:
            patrol_alt = feet(25000)

        builder = WaypointBuilder(flight, self.coalition)
        orbit = builder.orbit(orbit_location, patrol_alt)

        return AwacsFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            nav_to=builder.nav_path(
                flight.departure.position, orbit.position, patrol_alt
            ),
            nav_from=builder.nav_path(
                orbit.position, flight.arrival.position, patrol_alt
            ),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
            hold=orbit,
            hold_duration=timedelta(hours=4),
        )

    def generate_bai(self, flight: Flight) -> FlightPlan:
        """Generates a BAI flight plan.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        from game.transfers import Convoy

        targets: List[StrikeTarget] = []
        if isinstance(location, TheaterGroundObject):
            for group in location.groups:
                if group.units:
                    targets.append(
                        StrikeTarget(f"{group.name} at {location.name}", group)
                    )
        elif isinstance(location, Convoy):
            targets.append(StrikeTarget(location.name, location))
        else:
            raise InvalidObjectiveLocation(flight.flight_type, location)

        return self.strike_flightplan(
            flight, location, FlightWaypointType.INGRESS_BAI, targets
        )

    @staticmethod
    def anti_ship_targets_for_tgo(tgo: NavalGroundObject) -> List[StrikeTarget]:
        return [StrikeTarget(f"{g.name} at {tgo.name}", g) for g in tgo.groups]

    def generate_anti_ship(self, flight: Flight) -> StrikeFlightPlan:
        """Generates an anti-ship flight plan.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        from game.transfers import CargoShip

        if isinstance(location, NavalControlPoint):
            targets = self.anti_ship_targets_for_tgo(location.find_main_tgo())
        elif isinstance(location, NavalGroundObject):
            targets = self.anti_ship_targets_for_tgo(location)
        elif isinstance(location, CargoShip):
            targets = [StrikeTarget(location.name, location)]
        else:
            raise InvalidObjectiveLocation(flight.flight_type, location)

        return self.strike_flightplan(
            flight, location, FlightWaypointType.INGRESS_BAI, targets
        )

    def generate_barcap(self, flight: Flight) -> BarCapFlightPlan:
        """Generate a BARCAP flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        start_pos, end_pos = self.racetrack_for_objective(location, barcap=True)
        patrol_alt = meters(
            random.randint(
                int(self.doctrine.min_patrol_altitude.meters),
                int(self.doctrine.max_patrol_altitude.meters),
            )
        )

        builder = WaypointBuilder(flight, self.coalition)
        start, end = builder.race_track(start_pos, end_pos, patrol_alt)

        return BarCapFlightPlan(
            package=self.package,
            flight=flight,
            patrol_duration=self.doctrine.cap_duration,
            engagement_distance=self.doctrine.cap_engagement_range,
            takeoff=builder.takeoff(flight.departure),
            nav_to=builder.nav_path(
                flight.departure.position, start.position, patrol_alt
            ),
            nav_from=builder.nav_path(
                end.position, flight.arrival.position, patrol_alt
            ),
            patrol_start=start,
            patrol_end=end,
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
        )

    def generate_sweep(self, flight: Flight) -> SweepFlightPlan:
        """Generate a BARCAP flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        assert self.package.waypoints is not None
        target = self.package.target.position
        heading = Heading.from_degrees(
            self.package.waypoints.join.heading_between_point(target)
        )
        start_pos = target.point_from_heading(
            heading.degrees, -self.doctrine.sweep_distance.meters
        )

        builder = WaypointBuilder(flight, self.coalition)
        start, end = builder.sweep(start_pos, target, self.doctrine.ingress_altitude)

        hold = builder.hold(self._hold_point(flight))

        return SweepFlightPlan(
            package=self.package,
            flight=flight,
            lead_time=timedelta(minutes=5),
            takeoff=builder.takeoff(flight.departure),
            hold=hold,
            hold_duration=timedelta(minutes=5),
            nav_to=builder.nav_path(
                hold.position, start.position, self.doctrine.ingress_altitude
            ),
            nav_from=builder.nav_path(
                end.position, flight.arrival.position, self.doctrine.ingress_altitude
            ),
            sweep_start=start,
            sweep_end=end,
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
        )

    def generate_transport(self, flight: Flight) -> AirliftFlightPlan:
        """Generate an airlift flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        cargo = flight.cargo
        if cargo is None:
            raise PlanningError(
                "Cannot plan transport mission for flight with no cargo."
            )

        altitude = feet(1500)
        altitude_is_agl = True

        builder = WaypointBuilder(flight, self.coalition)

        pickup = None
        nav_to_pickup = []
        if cargo.origin != flight.departure:
            pickup = builder.pickup(cargo.origin)
            nav_to_pickup = builder.nav_path(
                flight.departure.position,
                cargo.origin.position,
                altitude,
                altitude_is_agl,
            )

        return AirliftFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            nav_to_pickup=nav_to_pickup,
            pickup=pickup,
            nav_to_drop_off=builder.nav_path(
                cargo.origin.position,
                cargo.next_stop.position,
                altitude,
                altitude_is_agl,
            ),
            drop_off=builder.drop_off(cargo.next_stop),
            nav_to_home=builder.nav_path(
                cargo.origin.position,
                flight.arrival.position,
                altitude,
                altitude_is_agl,
            ),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
        )

    def racetrack_for_objective(
        self, location: MissionTarget, barcap: bool
    ) -> Tuple[Point, Point]:
        closest_cache = ObjectiveDistanceCache.get_closest_airfields(location)
        for airfield in closest_cache.operational_airfields:
            # If the mission is a BARCAP of an enemy airfield, find the *next*
            # closest enemy airfield.
            if airfield == self.package.target:
                continue
            if airfield.captured != self.is_player:
                closest_airfield = airfield
                break
        else:
            raise PlanningError("Could not find any enemy airfields")

        heading = Heading.from_degrees(
            location.position.heading_between_point(closest_airfield.position)
        )

        position = ShapelyPoint(
            self.package.target.position.x, self.package.target.position.y
        )

        if barcap:
            # BARCAPs should remain far enough back from the enemy that their
            # commit range does not enter the enemy's threat zone. Include a 5nm
            # buffer.
            distance_to_no_fly = (
                meters(position.distance(self.threat_zones.all))
                - self.doctrine.cap_engagement_range
                - nautical_miles(5)
            )
        else:
            # Other race tracks (TARCAPs, currently) just try to keep some
            # distance from the nearest enemy airbase, but since they are by
            # definition in enemy territory they can't avoid the threat zone
            # without being useless.
            min_distance_from_enemy = nautical_miles(20)
            distance_to_airfield = meters(
                closest_airfield.position.distance_to_point(
                    self.package.target.position
                )
            )
            distance_to_no_fly = distance_to_airfield - min_distance_from_enemy

        min_cap_distance = min(
            self.doctrine.cap_min_distance_from_cp, distance_to_no_fly
        )
        max_cap_distance = min(
            self.doctrine.cap_max_distance_from_cp, distance_to_no_fly
        )

        end = location.position.point_from_heading(
            heading.degrees,
            random.randint(int(min_cap_distance.meters), int(max_cap_distance.meters)),
        )
        diameter = random.randint(
            int(self.doctrine.cap_min_track_length.meters),
            int(self.doctrine.cap_max_track_length.meters),
        )
        start = end.point_from_heading(heading.opposite.degrees, diameter)
        return start, end

    def aewc_orbit(self, location: MissionTarget) -> Point:
        closest_boundary = self.threat_zones.closest_boundary(location.position)
        heading_to_threat_boundary = Heading.from_degrees(
            location.position.heading_between_point(closest_boundary)
        )
        distance_to_threat = meters(
            location.position.distance_to_point(closest_boundary)
        )
        orbit_heading = heading_to_threat_boundary
        # Station 100nm outside the threat zone.
        threat_buffer = nautical_miles(100)
        if self.threat_zones.threatened(location.position):
            orbit_distance = distance_to_threat + threat_buffer
        else:
            orbit_distance = distance_to_threat - threat_buffer

        return location.position.point_from_heading(
            orbit_heading.degrees, orbit_distance.meters
        )

    def racetrack_for_frontline(
        self, origin: Point, front_line: FrontLine
    ) -> Tuple[Point, Point]:
        # Find targets waypoints
        ingress, heading, distance = Conflict.frontline_vector(front_line, self.theater)
        center = ingress.point_from_heading(heading.degrees, distance / 2)
        orbit_center = center.point_from_heading(
            heading.left.degrees,
            random.randint(
                int(nautical_miles(6).meters), int(nautical_miles(15).meters)
            ),
        )

        combat_width = distance / 2
        if combat_width > 500000:
            combat_width = 500000
        if combat_width < 35000:
            combat_width = 35000

        radius = combat_width * 1.25
        start = orbit_center.point_from_heading(heading.degrees, radius)
        end = orbit_center.point_from_heading(heading.opposite.degrees, radius)

        if end.distance_to_point(origin) < start.distance_to_point(origin):
            start, end = end, start
        return start, end

    def generate_tarcap(self, flight: Flight) -> TarCapFlightPlan:
        """Generate a CAP flight plan for the given front line.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        patrol_alt = meters(
            random.randint(
                int(self.doctrine.min_patrol_altitude.meters),
                int(self.doctrine.max_patrol_altitude.meters),
            )
        )

        # Create points
        builder = WaypointBuilder(flight, self.coalition)

        if isinstance(location, FrontLine):
            orbit0p, orbit1p = self.racetrack_for_frontline(
                flight.departure.position, location
            )
        else:
            orbit0p, orbit1p = self.racetrack_for_objective(location, barcap=False)

        start, end = builder.race_track(orbit0p, orbit1p, patrol_alt)
        return TarCapFlightPlan(
            package=self.package,
            flight=flight,
            lead_time=timedelta(minutes=2),
            # Note that this duration only has an effect if there are no
            # flights in the package that have requested escort. If the package
            # requests an escort the CAP flight will remain on station for the
            # duration of the escorted mission, or until it is winchester/bingo.
            patrol_duration=self.doctrine.cap_duration,
            engagement_distance=self.doctrine.cap_engagement_range,
            takeoff=builder.takeoff(flight.departure),
            nav_to=builder.nav_path(flight.departure.position, orbit0p, patrol_alt),
            nav_from=builder.nav_path(orbit1p, flight.arrival.position, patrol_alt),
            patrol_start=start,
            patrol_end=end,
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
        )

    def generate_dead(
        self, flight: Flight, custom_targets: Optional[List[Unit]]
    ) -> StrikeFlightPlan:
        """Generate a DEAD flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            custom_targets: Specific radar equipped units selected by the user.
        """
        location = self.package.target

        is_ewr = isinstance(location, EwrGroundObject)
        is_sam = isinstance(location, SamGroundObject)
        if not is_ewr and not is_sam:
            logging.exception(
                f"Invalid Objective Location for DEAD flight {flight=} at {location=}"
            )
            raise InvalidObjectiveLocation(flight.flight_type, location)

        # TODO: Unify these.
        # There doesn't seem to be any reason to treat the UI fragged missions
        # different from the automatic missions.
        targets: Optional[List[StrikeTarget]] = None
        if custom_targets is not None:
            targets = []
            for target in custom_targets:
                targets.append(StrikeTarget(location.name, target))

        return self.strike_flightplan(
            flight, location, FlightWaypointType.INGRESS_DEAD, targets
        )

    def generate_oca_strike(self, flight: Flight) -> StrikeFlightPlan:
        """Generate an OCA Strike flight plan at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if not isinstance(location, Airfield):
            logging.exception(
                f"Invalid Objective Location for OCA Strike flight "
                f"{flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(flight.flight_type, location)

        return self.strike_flightplan(
            flight, location, FlightWaypointType.INGRESS_OCA_AIRCRAFT
        )

    def generate_runway_attack(self, flight: Flight) -> StrikeFlightPlan:
        """Generate a runway attack flight plan at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if not isinstance(location, Airfield):
            logging.exception(
                f"Invalid Objective Location for runway bombing flight "
                f"{flight=} at {location=}."
            )
            raise InvalidObjectiveLocation(flight.flight_type, location)

        return self.strike_flightplan(
            flight, location, FlightWaypointType.INGRESS_OCA_RUNWAY
        )

    def generate_sead(
        self, flight: Flight, custom_targets: Optional[List[Unit]]
    ) -> StrikeFlightPlan:
        """Generate a SEAD flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            custom_targets: Specific radar equipped units selected by the user.
        """
        location = self.package.target

        # TODO: Unify these.
        # There doesn't seem to be any reason to treat the UI fragged missions
        # different from the automatic missions.
        targets: Optional[List[StrikeTarget]] = None
        if custom_targets is not None:
            targets = []
            for target in custom_targets:
                targets.append(StrikeTarget(location.name, target))

        return self.strike_flightplan(
            flight,
            location,
            FlightWaypointType.INGRESS_SEAD,
            targets,
            lead_time=timedelta(minutes=1),
        )

    def generate_escort(self, flight: Flight) -> StrikeFlightPlan:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(flight, self.coalition)
        ingress, target = builder.escort(
            self.package.waypoints.ingress, self.package.target
        )
        hold = builder.hold(self._hold_point(flight))
        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)

        return StrikeFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            hold=hold,
            hold_duration=timedelta(minutes=5),
            nav_to=builder.nav_path(
                hold.position, join.position, self.doctrine.ingress_altitude
            ),
            join=join,
            ingress=ingress,
            targets=[target],
            split=split,
            nav_from=builder.nav_path(
                split.position, flight.arrival.position, self.doctrine.ingress_altitude
            ),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
        )

    def generate_cas(self, flight: Flight) -> CasFlightPlan:
        """Generate a CAS flight plan for the given target.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        ingress, heading, distance = Conflict.frontline_vector(location, self.theater)
        center = ingress.point_from_heading(heading.degrees, distance / 2)
        egress = ingress.point_from_heading(heading.degrees, distance)

        ingress_distance = ingress.distance_to_point(flight.departure.position)
        egress_distance = egress.distance_to_point(flight.departure.position)
        if egress_distance < ingress_distance:
            ingress, egress = egress, ingress

        builder = WaypointBuilder(flight, self.coalition)

        return CasFlightPlan(
            package=self.package,
            flight=flight,
            patrol_duration=self.doctrine.cas_duration,
            takeoff=builder.takeoff(flight.departure),
            nav_to=builder.nav_path(
                flight.departure.position, ingress, self.doctrine.ingress_altitude
            ),
            nav_from=builder.nav_path(
                egress, flight.arrival.position, self.doctrine.ingress_altitude
            ),
            patrol_start=builder.ingress(
                FlightWaypointType.INGRESS_CAS, ingress, location
            ),
            engagement_distance=meters(FRONTLINE_LENGTH) / 2,
            target=builder.cas(center),
            patrol_end=builder.egress(egress, location),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
        )

    def generate_refueling_racetrack(self, flight: Flight) -> RefuelingFlightPlan:
        location = self.package.target

        closest_boundary = self.threat_zones.closest_boundary(location.position)
        heading_to_threat_boundary = Heading.from_degrees(
            location.position.heading_between_point(closest_boundary)
        )
        distance_to_threat = meters(
            location.position.distance_to_point(closest_boundary)
        )
        orbit_heading = heading_to_threat_boundary

        # Station 70nm outside the threat zone.
        threat_buffer = nautical_miles(70)
        if self.threat_zones.threatened(location.position):
            orbit_distance = distance_to_threat + threat_buffer
        else:
            orbit_distance = distance_to_threat - threat_buffer

        racetrack_center = location.position.point_from_heading(
            orbit_heading.degrees, orbit_distance.meters
        )

        racetrack_half_distance = Distance.from_nautical_miles(20).meters

        racetrack_start = racetrack_center.point_from_heading(
            orbit_heading.right.degrees, racetrack_half_distance
        )
        racetrack_end = racetrack_center.point_from_heading(
            orbit_heading.left.degrees, racetrack_half_distance
        )

        builder = WaypointBuilder(flight, self.coalition)

        tanker_type = flight.unit_type
        if tanker_type.patrol_altitude is not None:
            altitude = tanker_type.patrol_altitude
        else:
            altitude = feet(21000)

        if tanker_type.patrol_speed is not None:
            speed = tanker_type.patrol_speed
        else:
            # ~280 knots IAS at 21000.
            speed = knots(400)

        racetrack = builder.race_track(racetrack_start, racetrack_end, altitude)

        return RefuelingFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            nav_to=builder.nav_path(
                flight.departure.position, racetrack_start, altitude
            ),
            nav_from=builder.nav_path(racetrack_end, flight.arrival.position, altitude),
            patrol_start=racetrack[0],
            patrol_end=racetrack[1],
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
            patrol_duration=timedelta(hours=1),
            patrol_speed=speed,
            # TODO: Factor out a common base of the combat and non-combat race-tracks.
            # No harm in setting this, but we ought to clean up a bit.
            engagement_distance=meters(0),
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

    def _hold_point(self, flight: Flight) -> Point:
        assert self.package.waypoints is not None
        origin = flight.departure.position
        target = self.package.target.position
        join = self.package.waypoints.join
        ip = self.package.waypoints.ingress
        return HoldZoneGeometry(
            target, origin, ip, join, self.coalition, self.theater
        ).find_best_hold_point()

    # TODO: Make a model for the waypoint builder and use that in the UI.
    def generate_rtb_waypoint(
        self, flight: Flight, arrival: ControlPoint
    ) -> FlightWaypoint:
        """Generate RTB landing point.

        Args:
            flight: The flight to generate the landing waypoint for.
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(flight, self.coalition)
        return builder.land(arrival)

    def strike_flightplan(
        self,
        flight: Flight,
        location: MissionTarget,
        ingress_type: FlightWaypointType,
        targets: Optional[List[StrikeTarget]] = None,
        lead_time: timedelta = timedelta(),
    ) -> StrikeFlightPlan:
        assert self.package.waypoints is not None
        builder = WaypointBuilder(flight, self.coalition, targets)

        target_waypoints: List[FlightWaypoint] = []
        if targets is not None:
            for target in targets:
                target_waypoints.append(self.target_waypoint(flight, builder, target))
        else:
            target_waypoints.append(
                self.target_area_waypoint(flight, location, builder)
            )

        hold = builder.hold(self._hold_point(flight))
        join = builder.join(self.package.waypoints.join)
        split = builder.split(self.package.waypoints.split)

        return StrikeFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            hold=hold,
            hold_duration=timedelta(minutes=5),
            nav_to=builder.nav_path(
                hold.position, join.position, self.doctrine.ingress_altitude
            ),
            join=join,
            ingress=builder.ingress(
                ingress_type, self.package.waypoints.ingress, location
            ),
            targets=target_waypoints,
            split=split,
            nav_from=builder.nav_path(
                split.position, flight.arrival.position, self.doctrine.ingress_altitude
            ),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert),
            bullseye=builder.bullseye(),
            lead_time=lead_time,
        )

    def package_airfield(self) -> ControlPoint:
        # We'll always have a package, but if this is being planned via the UI
        # it could be the first flight in the package.
        if not self.package.flights:
            raise PlanningError(
                "Cannot determine source airfield for package with no flights"
            )

        # The package airfield is either the flight's airfield (when there is no
        # package) or the closest airfield to the objective that is the
        # departure airfield for some flight in the package.
        cache = ObjectiveDistanceCache.get_closest_airfields(self.package.target)
        for airfield in cache.operational_airfields:
            for flight in self.package.flights:
                if flight.departure == airfield:
                    return airfield
        raise PlanningError("Could not find any airfield assigned to this package")
