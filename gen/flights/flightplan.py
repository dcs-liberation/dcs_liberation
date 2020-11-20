"""Flight plan generation.

Flights are first planned generically by either the player or by the
MissionPlanner. Those only plan basic information like the objective, aircraft
type, and the size of the flight. The FlightPlanBuilder is responsible for
generating the waypoints for the mission.
"""
from __future__ import annotations

import math
from datetime import timedelta
from functools import cached_property
import logging
import random
from dataclasses import dataclass
from typing import Iterator, List, Optional, Set, TYPE_CHECKING, Tuple

from dcs.mapping import Point
from dcs.unit import Unit

from game.data.doctrine import Doctrine
from game.utils import nm_to_meter
from theater import (
    ControlPoint,
    FrontLine,
    MissionTarget,
    SamGroundObject,
    TheaterGroundObject,
)
from game.theater.theatergroundobject import EwrGroundObject
from .closestairfields import ObjectiveDistanceCache
from .flight import Flight, FlightType, FlightWaypoint, FlightWaypointType
from .traveltime import GroundSpeed, TravelTime
from .waypointbuilder import StrikeTarget, WaypointBuilder
from ..conflictgen import Conflict

if TYPE_CHECKING:
    from game import Game
    from gen.ato import Package


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
        super().__init__(
            f"{location.name} is not valid for {task.name} missions."
        )


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

    @property
    def edges(self) -> Iterator[Tuple[FlightWaypoint, FlightWaypoint]]:
        """A list of all paths between waypoints, in order."""
        return zip(self.waypoints, self.waypoints[1:])

    def best_speed_between_waypoints(self, a: FlightWaypoint,
                                     b: FlightWaypoint) -> int:
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
        return int(
            GroundSpeed.for_flight(self.flight, min(a.alt, b.alt)) * factor)

    def speed_between_waypoints(self, a: FlightWaypoint,
                                b: FlightWaypoint) -> int:
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
    def tot_offset(self) -> timedelta:
        """This flight's offset from the package's TOT.

        Positive values represent later TOTs. An offset of -2 minutes is used
        for a flight that has a TOT 2 minutes before the rest of the package.
        """
        return timedelta()

    # Not cached because changes to the package might alter the formation speed.
    @property
    def travel_time_to_target(self) -> Optional[timedelta]:
        """The estimated time between the first waypoint and the target."""
        if self.tot_waypoint is None:
            return None
        return self._travel_time_to_waypoint(self.tot_waypoint)

    def _travel_time_to_waypoint(
            self, destination: FlightWaypoint) -> timedelta:
        total = timedelta()
        for previous_waypoint, waypoint in self.edges:
            total += self.travel_time_between_waypoints(previous_waypoint,
                                                        waypoint)
            if waypoint == destination:
                break
        else:
            raise PlanningError(
                f"Did not find destination waypoint {destination} in "
                f"waypoints for {self.flight}")
        return total

    def travel_time_between_waypoints(self, a: FlightWaypoint,
                                      b: FlightWaypoint) -> timedelta:
        return TravelTime.between_points(a.position, b.position,
                                         self.speed_between_waypoints(a, b))

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        raise NotImplementedError

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        raise NotImplementedError

    def request_escort_at(self) -> Optional[FlightWaypoint]:
        return None

    def dismiss_escort_at(self) -> Optional[FlightWaypoint]:
        return None


@dataclass(frozen=True)
class LoiterFlightPlan(FlightPlan):
    hold: FlightWaypoint

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

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.hold:
            return self.push_time
        return None


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
    def best_flight_formation_speed(self) -> int:
        """The best speed this flight is capable at all formation waypoints.

        To ease coordination with other flights, we aim to have a single mission
        speed used by the formation for all waypoints. As such, this function
        returns the highest ground speed that the flight is capable of flying at
        all of its formation waypoints.
        """
        speeds = []
        for previous_waypoint, waypoint in self.edges:
            if waypoint in self.package_speed_waypoints:
                speeds.append(self.best_speed_between_waypoints(
                    previous_waypoint, waypoint))
        return min(speeds)

    def speed_between_waypoints(self, a: FlightWaypoint,
                                b: FlightWaypoint) -> int:
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
            GroundSpeed.for_flight(self.flight, self.hold.alt)
        )


@dataclass(frozen=True)
class PatrollingFlightPlan(FlightPlan):
    patrol_start: FlightWaypoint
    patrol_end: FlightWaypoint

    #: Maximum time to remain on station.
    patrol_duration: timedelta

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

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
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


@dataclass(frozen=True)
class BarCapFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from [
            self.takeoff,
            self.patrol_start,
            self.patrol_end,
            self.land,
        ]
        if self.divert is not None:
            yield self.divert


@dataclass(frozen=True)
class CasFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    target: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from [
            self.takeoff,
            self.patrol_start,
            self.target,
            self.patrol_end,
            self.land,
        ]
        if self.divert is not None:
            yield self.divert

    def request_escort_at(self) -> Optional[FlightWaypoint]:
        return self.patrol_start

    def dismiss_escort_at(self) -> Optional[FlightWaypoint]:
        return self.patrol_end


@dataclass(frozen=True)
class TarCapFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    lead_time: timedelta

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from [
            self.takeoff,
            self.patrol_start,
            self.patrol_end,
            self.land,
        ]
        if self.divert is not None:
            yield self.divert

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.patrol_end:
            return self.patrol_end_time
        return super().depart_time_for_waypoint(waypoint)

    @property
    def patrol_start_time(self) -> timedelta:
        start = self.package.escort_start_time
        if start is not None:
            return start + self.tot_offset
        return super().patrol_start_time + self.tot_offset

    @property
    def patrol_end_time(self) -> timedelta:
        end = self.package.escort_end_time
        if end is not None:
            return end
        return super().patrol_end_time


# TODO: Remove when breaking save compat.
FrontLineCapFlightPlan = TarCapFlightPlan


@dataclass(frozen=True)
class StrikeFlightPlan(FormationFlightPlan):
    takeoff: FlightWaypoint
    hold: FlightWaypoint
    join: FlightWaypoint
    ingress: FlightWaypoint
    targets: List[FlightWaypoint]
    egress: FlightWaypoint
    split: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from [
            self.takeoff,
            self.hold,
            self.join,
            self.ingress
        ]
        yield from self.targets
        yield from[
            self.egress,
            self.split,
            self.land,
        ]
        if self.divert is not None:
            yield self.divert

    @property
    def package_speed_waypoints(self) -> Set[FlightWaypoint]:
        return {
            self.ingress,
            self.egress,
            self.split,
        } | set(self.targets)

    def speed_between_waypoints(self, a: FlightWaypoint,
                                b: FlightWaypoint) -> int:
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
    def target_area_waypoint(self) -> FlightWaypoint:
        return FlightWaypoint(FlightWaypointType.TARGET_GROUP_LOC,
                              self.package.target.position.x,
                              self.package.target.position.y, 0)

    @property
    def travel_time_to_target(self) -> timedelta:
        """The estimated time between the first waypoint and the target."""
        destination = self.tot_waypoint
        total = timedelta()
        for previous_waypoint, waypoint in self.edges:
            if waypoint == self.tot_waypoint:
                # For anything strike-like the TOT waypoint is the *flight's*
                # mission target, but to synchronize with the rest of the
                # package we need to use the travel time to the same position as
                # the others.
                total += self.travel_time_between_waypoints(
                    previous_waypoint, self.target_area_waypoint)
                break
            total += self.travel_time_between_waypoints(previous_waypoint,
                                                        waypoint)
        else:
            raise PlanningError(
                f"Did not find destination waypoint {destination} in "
                f"waypoints for {self.flight}")
        return total

    @property
    def mission_speed(self) -> int:
        return GroundSpeed.for_flight(self.flight, self.ingress.alt)

    @property
    def join_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.join, self.ingress)
        return self.ingress_time - travel_time

    @property
    def split_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.egress, self.split)
        return self.egress_time + travel_time

    @property
    def ingress_time(self) -> timedelta:
        tot = self.package.time_over_target
        travel_time = self.travel_time_between_waypoints(
            self.ingress, self.target_area_waypoint)
        return tot - travel_time

    @property
    def egress_time(self) -> timedelta:
        tot = self.package.time_over_target
        travel_time = self.travel_time_between_waypoints(
            self.target_area_waypoint, self.egress)
        return tot + travel_time

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.ingress:
            return self.ingress_time
        elif waypoint == self.egress:
            return self.egress_time
        elif waypoint in self.targets:
            return self.package.time_over_target
        return super().tot_for_waypoint(waypoint)


@dataclass(frozen=True)
class SweepFlightPlan(LoiterFlightPlan):
    takeoff: FlightWaypoint
    sweep_start: FlightWaypoint
    sweep_end: FlightWaypoint
    land: FlightWaypoint
    divert: Optional[FlightWaypoint]
    lead_time: timedelta

    def iter_waypoints(self) -> Iterator[FlightWaypoint]:
        yield from [
            self.takeoff,
            self.hold,
            self.sweep_start,
            self.sweep_end,
            self.land,
        ]
        if self.divert is not None:
            yield self.divert

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        return self.sweep_end

    @property
    def tot_offset(self) -> timedelta:
        return -self.lead_time

    @property
    def sweep_start_time(self) -> timedelta:
        travel_time = self.travel_time_between_waypoints(
            self.sweep_start, self.sweep_end)
        return self.sweep_end_time - travel_time

    @property
    def sweep_end_time(self) -> timedelta:
        return self.package.time_over_target + self.tot_offset

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.sweep_start:
            return self.sweep_start_time
        if waypoint == self.sweep_end:
            return self.sweep_end_time
        return None

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.hold:
            return self.push_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.sweep_end_time - TravelTime.between_points(
            self.hold.position,
            self.sweep_end.position,
            GroundSpeed.for_flight(self.flight, self.hold.alt)
        )


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

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        return None


class FlightPlanBuilder:
    """Generates flight plans for flights."""

    def __init__(self, game: Game, package: Package, is_player: bool) -> None:
        # TODO: Plan similar altitudes for the in-country leg of the mission.
        # Waypoint altitudes for a given flight *shouldn't* differ too much
        # between the join and split points, so we don't need speeds for each
        # leg individually since they should all be fairly similar. This doesn't
        # hold too well right now since nothing is stopping each waypoint from
        # jumping 20k feet each time, but that's a huge waste of energy we
        # should be avoiding anyway.
        self.game = game
        self.package = package
        self.is_player = is_player
        if is_player:
            faction = self.game.player_faction
        else:
            faction = self.game.enemy_faction
        self.doctrine: Doctrine = faction.doctrine

    def populate_flight_plan(
            self, flight: Flight,
            # TODO: Custom targets should be an attribute of the flight.
            custom_targets: Optional[List[Unit]] = None) -> None:
        """Creates a default flight plan for the given mission."""
        if flight not in self.package.flights:
            raise RuntimeError("Flight must be a part of the package")
        if self.package.waypoints is None:
            self.regenerate_package_waypoints()
        flight.flight_plan = self.generate_flight_plan(flight, custom_targets)

    def generate_flight_plan(
            self, flight: Flight,
            custom_targets: Optional[List[Unit]]) -> FlightPlan:
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
        elif task == FlightType.SEAD:
            return self.generate_sead(flight, custom_targets)
        elif task == FlightType.STRIKE:
            return self.generate_strike(flight)
        elif task == FlightType.SWEEP:
            return self.generate_sweep(flight)
        elif task == FlightType.TARCAP:
            return self.generate_tarcap(flight)
        elif task == FlightType.TROOP_TRANSPORT:
            logging.error(
                "Troop transport flight plan generation not implemented"
            )
        raise PlanningError(
            f"{task.name} flight plan generation not implemented")

    def regenerate_package_waypoints(self) -> None:
        ingress_point = self._ingress_point()
        egress_point = self._egress_point()
        join_point = self._rendezvous_point(ingress_point)
        split_point = self._rendezvous_point(egress_point)

        from gen.ato import PackageWaypoints
        self.package.waypoints = PackageWaypoints(
            join_point,
            ingress_point,
            egress_point,
            split_point,
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
        if len(location.groups) > 0 and location.dcs_identifier == "AA":
            # TODO: Replace with DEAD?
            # Strike missions on SEAD targets target units.
            for g in location.groups:
                for j, u in enumerate(g.units):
                    targets.append(StrikeTarget(f"{u.type} #{j}", u))
        else:
            # TODO: Does this actually happen?
            # ConflictTheater is built with the belief that multiple ground
            # objects have the same name. If that's the case,
            # TheaterGroundObject needs some refactoring because it behaves very
            # differently for SAM sites than it does for strike targets.
            buildings = self.game.theater.find_ground_objects_by_obj_name(
                location.obj_name
            )
            for building in buildings:
                if building.is_dead:
                    continue

                targets.append(StrikeTarget(building.category, building))

        return self.strike_flightplan(flight, location, targets)

    def generate_bai(self, flight: Flight) -> StrikeFlightPlan:
        """Generates a BAI flight plan.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        targets: List[StrikeTarget] = []
        for group in location.groups:
            targets.append(
                StrikeTarget(f"{group.name} at {location.name}", group))

        return self.strike_flightplan(flight, location, targets)

    def generate_anti_ship(self, flight: Flight) -> StrikeFlightPlan:
        """Generates an anti-ship flight plan.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if isinstance(location, ControlPoint):
            if location.is_fleet:
                # The first group generated will be the carrier group itself.
                location = location.ground_objects[0]
            else:
                raise InvalidObjectiveLocation(flight.flight_type, location)

        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        targets: List[StrikeTarget] = []
        for group in location.groups:
            targets.append(
                StrikeTarget(f"{group.name} at {location.name}", group))

        return self.strike_flightplan(flight, location, targets)

    def generate_barcap(self, flight: Flight) -> BarCapFlightPlan:
        """Generate a BARCAP flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        start, end = self.racetrack_for_objective(location)
        patrol_alt = random.randint(
            self.doctrine.min_patrol_altitude,
            self.doctrine.max_patrol_altitude
        )

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        start, end = builder.race_track(start, end, patrol_alt)

        return BarCapFlightPlan(
            package=self.package,
            flight=flight,
            patrol_duration=self.doctrine.cap_duration,
            takeoff=builder.takeoff(flight.departure),
            patrol_start=start,
            patrol_end=end,
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert)
        )

    def generate_sweep(self, flight: Flight) -> SweepFlightPlan:
        """Generate a BARCAP flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        target = self.package.target.position

        heading = self._heading_to_package_airfield(target)
        start = target.point_from_heading(heading,
                                          -self.doctrine.sweep_distance)

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        start, end = builder.sweep(start, target,
                                   self.doctrine.ingress_altitude)

        return SweepFlightPlan(
            package=self.package,
            flight=flight,
            lead_time=timedelta(minutes=5),
            takeoff=builder.takeoff(flight.departure),
            hold=builder.hold(self._hold_point(flight)),
            sweep_start=start,
            sweep_end=end,
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert)
        )

    def racetrack_for_objective(self,
                                location: MissionTarget) -> Tuple[Point, Point]:
        closest_cache = ObjectiveDistanceCache.get_closest_airfields(location)
        for airfield in closest_cache.closest_airfields:
            # If the mission is a BARCAP of an enemy airfield, find the *next*
            # closest enemy airfield.
            if airfield == self.package.target:
                continue
            if airfield.captured != self.is_player:
                closest_airfield = airfield
                break
        else:
            raise PlanningError("Could not find any enemy airfields")

        heading = location.position.heading_between_point(
            closest_airfield.position
        )

        min_distance_from_enemy = nm_to_meter(20)
        distance_to_airfield = int(closest_airfield.position.distance_to_point(
            self.package.target.position
        ))
        distance_to_no_fly = distance_to_airfield - min_distance_from_enemy
        min_cap_distance = min(self.doctrine.cap_min_distance_from_cp,
                               distance_to_no_fly)
        max_cap_distance = min(self.doctrine.cap_max_distance_from_cp,
                               distance_to_no_fly)

        end = location.position.point_from_heading(
            heading,
            random.randint(min_cap_distance, max_cap_distance)
        )
        diameter = random.randint(
            self.doctrine.cap_min_track_length,
            self.doctrine.cap_max_track_length
        )
        start = end.point_from_heading(heading - 180, diameter)
        return start, end

    def racetrack_for_frontline(self,
                                front_line: FrontLine) -> Tuple[Point, Point]:
        ally_cp, enemy_cp = front_line.control_points

        # Find targets waypoints
        ingress, heading, distance = Conflict.frontline_vector(
            ally_cp, enemy_cp, self.game.theater
        )
        center = ingress.point_from_heading(heading, distance / 2)
        orbit_center = center.point_from_heading(
            heading - 90, random.randint(nm_to_meter(6), nm_to_meter(15))
        )

        combat_width = distance / 2
        if combat_width > 500000:
            combat_width = 500000
        if combat_width < 35000:
            combat_width = 35000

        radius = combat_width*1.25
        orbit0p = orbit_center.point_from_heading(heading, radius)
        orbit1p = orbit_center.point_from_heading(heading + 180, radius)

        return orbit0p, orbit1p

    def generate_tarcap(self, flight: Flight) -> TarCapFlightPlan:
        """Generate a CAP flight plan for the given front line.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        patrol_alt = random.randint(self.doctrine.min_patrol_altitude,
                                    self.doctrine.max_patrol_altitude)

        # Create points
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)

        if isinstance(location, FrontLine):
            orbit0p, orbit1p = self.racetrack_for_frontline(location)
        else:
            orbit0p, orbit1p = self.racetrack_for_objective(location)

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
            takeoff=builder.takeoff(flight.departure),
            patrol_start=start,
            patrol_end=end,
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert)
        )

    def generate_dead(self, flight: Flight,
                      custom_targets: Optional[List[Unit]]) -> StrikeFlightPlan:
        """Generate a DEAD flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            custom_targets: Specific radar equipped units selected by the user.
        """
        location = self.package.target

        is_ewr = isinstance(location, EwrGroundObject)
        is_sam = isinstance(location, SamGroundObject)
        if not is_ewr and not is_sam:
            logging.exception(f"Invalid Objective Location for DEAD flight {flight=} at {location=}")
            raise InvalidObjectiveLocation(flight.flight_type, location)

        # TODO: Unify these.
        # There doesn't seem to be any reason to treat the UI fragged missions
        # different from the automatic missions.
        targets: Optional[List[StrikeTarget]] = None
        if custom_targets is not None:
            targets = []
            for target in custom_targets:
                targets.append(StrikeTarget(location.name, target))

        return self.strike_flightplan(flight, location, targets)

    def generate_sead(self, flight: Flight,
                      custom_targets: Optional[List[Unit]]) -> StrikeFlightPlan:
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

        return self.strike_flightplan(flight, location, targets)

    def generate_escort(self, flight: Flight) -> StrikeFlightPlan:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        ingress, target, egress = builder.escort(
            self.package.waypoints.ingress, self.package.target,
            self.package.waypoints.egress)

        return StrikeFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            hold=builder.hold(self._hold_point(flight)),
            join=builder.join(self.package.waypoints.join),
            ingress=ingress,
            targets=[target],
            egress=egress,
            split=builder.split(self.package.waypoints.split),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert)
        )

    def generate_cas(self, flight: Flight) -> CasFlightPlan:
        """Generate a CAS flight plan for the given target.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        ingress, heading, distance = Conflict.frontline_vector(
            location.control_points[0], location.control_points[1],
            self.game.theater
        )
        center = ingress.point_from_heading(heading, distance / 2)
        egress = ingress.point_from_heading(heading, distance)

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)

        return CasFlightPlan(
            package=self.package,
            flight=flight,
            patrol_duration=self.doctrine.cas_duration,
            takeoff=builder.takeoff(flight.departure),
            patrol_start=builder.ingress_cas(ingress, location),
            target=builder.cas(center),
            patrol_end=builder.egress(egress, location),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert)
        )

    @staticmethod
    def target_waypoint(flight: Flight, builder: WaypointBuilder,
                        target: StrikeTarget) -> FlightWaypoint:
        if flight.flight_type in {FlightType.ANTISHIP, FlightType.BAI}:
            return builder.bai_group(target)
        elif flight.flight_type == FlightType.DEAD:
            return builder.dead_point(target)
        elif flight.flight_type == FlightType.SEAD:
            return builder.sead_point(target)
        else:
            return builder.strike_point(target)

    @staticmethod
    def target_area_waypoint(flight: Flight, location: MissionTarget,
                             builder: WaypointBuilder) -> FlightWaypoint:
        if flight.flight_type == FlightType.DEAD:
            return builder.dead_area(location)
        elif flight.flight_type == FlightType.SEAD:
            return builder.sead_area(location)
        else:
            return builder.strike_area(location)

    def _hold_point(self, flight: Flight) -> Point:
        assert self.package.waypoints is not None
        origin = flight.departure.position
        target = self.package.target.position
        join = self.package.waypoints.join
        origin_to_target = origin.distance_to_point(target)
        join_to_target = join.distance_to_point(target)
        if origin_to_target < join_to_target:
            # If the origin airfield is closer to the target than the join
            # point, plan the hold point such that it retreats from the origin
            # airfield.
            return join.point_from_heading(target.heading_between_point(origin),
                                           self.doctrine.push_distance)

        heading_to_join = origin.heading_between_point(join)
        hold_point = origin.point_from_heading(heading_to_join,
                                               self.doctrine.push_distance)
        if hold_point.distance_to_point(join) >= self.doctrine.push_distance:
            # Hold point is between the origin airfield and the join point and
            # spaced sufficiently.
            return hold_point

        # The hold point is between the origin airfield and the join point, but
        # the distance between the hold point and the join point is too short.
        # Bend the hold point out to extend the distance while maintaining the
        # minimum distance from the origin airfield to keep the AI flying
        # properly.
        origin_to_join = origin.distance_to_point(join)
        cos_theta = (
                (self.doctrine.hold_distance ** 2 +
                 origin_to_join ** 2 -
                 self.doctrine.join_distance ** 2) /
                (2 * self.doctrine.hold_distance * origin_to_join)
        )
        try:
            theta = math.acos(cos_theta)
        except ValueError:
            # No solution that maintains hold and join distances. Extend the
            # hold point away from the target.
            return origin.point_from_heading(
                target.heading_between_point(origin),
                self.doctrine.hold_distance)

        return origin.point_from_heading(heading_to_join - theta,
                                         self.doctrine.hold_distance)

    # TODO: Make a model for the waypoint builder and use that in the UI.
    def generate_rtb_waypoint(self, flight: Flight,
                              arrival: ControlPoint) -> FlightWaypoint:
        """Generate RTB landing point.

        Args:
            flight: The flight to generate the landing waypoint for.
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        return builder.land(arrival)

    def strike_flightplan(
            self, flight: Flight, location: MissionTarget,
            targets: Optional[List[StrikeTarget]] = None) -> StrikeFlightPlan:
        assert self.package.waypoints is not None
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine,
                                  targets)
        if flight.flight_type is FlightType.SEAD:
            ingress = builder.ingress_sead(self.package.waypoints.ingress,
                                           location)

        elif flight.flight_type is FlightType.DEAD:
            ingress = builder.ingress_dead(self.package.waypoints.ingress,
                                           location)
        elif flight.flight_type in {FlightType.ANTISHIP, FlightType.BAI}:
            ingress = builder.ingress_bai(self.package.waypoints.ingress,
                                          location)
        else:
            ingress = builder.ingress_strike(self.package.waypoints.ingress,
                                             location)

        target_waypoints: List[FlightWaypoint] = []
        if targets is not None:
            for target in targets:
                target_waypoints.append(
                    self.target_waypoint(flight, builder, target))
        else:
            target_waypoints.append(
                self.target_area_waypoint(flight, location, builder))

        return StrikeFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.departure),
            hold=builder.hold(self._hold_point(flight)),
            join=builder.join(self.package.waypoints.join),
            ingress=ingress,
            targets=target_waypoints,
            egress=builder.egress(self.package.waypoints.egress, location),
            split=builder.split(self.package.waypoints.split),
            land=builder.land(flight.arrival),
            divert=builder.divert(flight.divert)
        )

    def _retreating_rendezvous_point(self, attack_transition: Point) -> Point:
        """Creates a rendezvous point that retreats from the origin airfield."""
        return attack_transition.point_from_heading(
            self.package.target.position.heading_between_point(
                self.package_airfield().position),
            self.doctrine.join_distance)

    def _advancing_rendezvous_point(self, attack_transition: Point) -> Point:
        """Creates a rendezvous point that advances toward the target."""
        heading = self._heading_to_package_airfield(attack_transition)
        return attack_transition.point_from_heading(
            heading, -self.doctrine.join_distance)

    def _rendezvous_should_retreat(self, attack_transition: Point) -> bool:
        transition_target_distance = attack_transition.distance_to_point(
            self.package.target.position
        )
        origin_target_distance = self._distance_to_package_airfield(
            self.package.target.position
        )

        # If the origin point is closer to the target than the ingress point,
        # the rendezvous point should be positioned in a position that retreats
        # from the origin airfield.
        return origin_target_distance < transition_target_distance

    def _rendezvous_point(self, attack_transition: Point) -> Point:
        """Returns the position of the rendezvous point.

        Args:
            attack_transition: The ingress or egress point for this rendezvous.
        """
        if self._rendezvous_should_retreat(attack_transition):
            return self._retreating_rendezvous_point(attack_transition)
        return self._advancing_rendezvous_point(attack_transition)

    def _ingress_point(self) -> Point:
        heading = self._target_heading_to_package_airfield()
        return self.package.target.position.point_from_heading(
            heading - 180 + 25, self.doctrine.ingress_egress_distance
        )

    def _egress_point(self) -> Point:
        heading = self._target_heading_to_package_airfield()
        return self.package.target.position.point_from_heading(
            heading - 180 - 25, self.doctrine.ingress_egress_distance
        )

    def _target_heading_to_package_airfield(self) -> int:
        return self._heading_to_package_airfield(self.package.target.position)

    def _heading_to_package_airfield(self, point: Point) -> int:
        return self.package_airfield().position.heading_between_point(point)

    def _distance_to_package_airfield(self, point: Point) -> int:
        return self.package_airfield().position.distance_to_point(point)

    def package_airfield(self) -> ControlPoint:
        # We'll always have a package, but if this is being planned via the UI
        # it could be the first flight in the package.
        if not self.package.flights:
            raise RuntimeError(
                "Cannot determine source airfield for package with no flights"
            )

        # The package airfield is either the flight's airfield (when there is no
        # package) or the closest airfield to the objective that is the
        # departure airfield for some flight in the package.
        cache = ObjectiveDistanceCache.get_closest_airfields(
            self.package.target
        )
        for airfield in cache.closest_airfields:
            for flight in self.package.flights:
                if flight.departure == airfield:
                    return airfield
        raise RuntimeError(
            "Could not find any airfield assigned to this package"
        )
