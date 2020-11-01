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
from theater import ControlPoint, FrontLine, MissionTarget, TheaterGroundObject
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
class PackageWaypointTiming:
    #: The package being scheduled.
    package: Package

    #: The package join time.
    join: timedelta

    #: The ingress waypoint TOT.
    ingress: timedelta

    #: The egress waypoint TOT.
    egress: timedelta

    #: The package split time.
    split: timedelta

    @property
    def target(self) -> timedelta:
        """The package time over target."""
        return self.package.time_over_target

    @classmethod
    def for_package(cls, package: Package) -> Optional[PackageWaypointTiming]:
        """Computes and returns the timings for package formation waypoints.

        Package waypoint timing depends on the composition of the package.
        Whenever flights are added or removed they must be recomputed since the
        mission speed may have changed.

        If the package contains no flights with formation flight plans, this
        returns None.
        """
        assert package.waypoints is not None

        if not package.flights:
            raise ValueError("Cannot plan TOT for package with no flights")

        group_ground_speed = package.formation_speed
        if group_ground_speed is None:
            return None

        # Round each waypoint TOT since DCS doesn't support sub-second timing
        # and it's not interesting to the user.
        ingress = timedelta(seconds=math.floor(
            (package.time_over_target - TravelTime.between_points(
                package.waypoints.ingress,
                package.target.position,
                group_ground_speed)).total_seconds()))

        join = timedelta(seconds=math.floor(
            (ingress - TravelTime.between_points(
                package.waypoints.join,
                package.waypoints.ingress,
                group_ground_speed)).total_seconds()))

        egress = timedelta(seconds=math.floor(
            (package.time_over_target + TravelTime.between_points(
                package.target.position,
                package.waypoints.egress,
                group_ground_speed)).total_seconds()))

        split = timedelta(seconds=math.floor(
            (egress + TravelTime.between_points(
                package.waypoints.egress,
                package.waypoints.split,
                group_ground_speed)).total_seconds()))

        return cls(package, join, ingress, egress, split)


@dataclass(frozen=True)
class FlightPlan:
    package: Package
    flight: Flight

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        """A list of all waypoints in the flight plan, in order."""
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
            total += TravelTime.between_points(
                previous_waypoint.position, waypoint.position,
                self.speed_between_waypoints(previous_waypoint, waypoint))
            if waypoint == destination:
                break
        else:
            raise PlanningError(
                f"Did not find destination waypoint {destination} in "
                f"waypoints for {self.flight}")
        return total

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
class FormationFlightPlan(FlightPlan):
    hold: FlightWaypoint
    join: FlightWaypoint
    split: FlightWaypoint

    @property
    def package_timing(self) -> PackageWaypointTiming:
        timing = PackageWaypointTiming.for_package(self.package)
        # Should be able to create a PackageWaypointTiming for any package with
        # a FormationFlightPlan flight.
        assert timing is not None
        return timing

    @property
    def waypoints(self) -> List[FlightWaypoint]:
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

    def tot_for_waypoint(self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        target_types = (
            FlightWaypointType.TARGET_GROUP_LOC,
            FlightWaypointType.TARGET_POINT,
            FlightWaypointType.TARGET_SHIP,
        )

        if waypoint.waypoint_type == FlightWaypointType.JOIN:
            return self.package_timing.join
        elif waypoint.waypoint_type in INGRESS_TYPES:
            return self.package_timing.ingress
        elif waypoint.waypoint_type in target_types:
            return self.package_timing.target
        elif waypoint.waypoint_type == FlightWaypointType.EGRESS:
            return self.package_timing.egress
        elif waypoint.waypoint_type == FlightWaypointType.SPLIT:
            return self.package_timing.split
        return None

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.hold:
            return self.push_time
        return None

    @property
    def push_time(self) -> timedelta:
        return self.package_timing.join - TravelTime.between_points(
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

    @property
    def waypoints(self) -> List[FlightWaypoint]:
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
    ascent: FlightWaypoint
    descent: FlightWaypoint
    land: FlightWaypoint

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        return [
            self.takeoff,
            self.ascent,
            self.patrol_start,
            self.patrol_end,
            self.descent,
            self.land,
        ]


@dataclass(frozen=True)
class CasFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    ascent: FlightWaypoint
    target: FlightWaypoint
    descent: FlightWaypoint
    land: FlightWaypoint

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        return [
            self.takeoff,
            self.ascent,
            self.patrol_start,
            self.target,
            self.patrol_end,
            self.descent,
            self.land,
        ]

    def request_escort_at(self) -> Optional[FlightWaypoint]:
        return self.patrol_start

    def dismiss_escort_at(self) -> Optional[FlightWaypoint]:
        return self.patrol_end


@dataclass(frozen=True)
class FrontLineCapFlightPlan(PatrollingFlightPlan):
    takeoff: FlightWaypoint
    ascent: FlightWaypoint
    descent: FlightWaypoint
    land: FlightWaypoint

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        return [
            self.takeoff,
            self.ascent,
            self.patrol_start,
            self.patrol_end,
            self.descent,
            self.land,
        ]

    def depart_time_for_waypoint(
            self, waypoint: FlightWaypoint) -> Optional[timedelta]:
        if waypoint == self.patrol_end:
            timing = PackageWaypointTiming.for_package(self.package)
            if timing is None:
                # If the player for some reason planned a TAR
                patrol_duration = self.patrol_duration
            else:
                patrol_duration = timing.egress
            return self.package.time_over_target + patrol_duration
        return super().depart_time_for_waypoint(waypoint)

    @property
    def patrol_start_time(self) -> timedelta:
        start = self.package.escort_start_time
        if start is not None:
            return start
        return super().patrol_start_time

    @property
    def patrol_end_time(self) -> timedelta:
        end = self.package.escort_end_time
        if end is not None:
            return end
        return super().patrol_end_time


@dataclass(frozen=True)
class StrikeFlightPlan(FormationFlightPlan):
    takeoff: FlightWaypoint
    ascent: FlightWaypoint
    hold: FlightWaypoint
    join: FlightWaypoint
    ingress: FlightWaypoint
    targets: List[FlightWaypoint]
    egress: FlightWaypoint
    split: FlightWaypoint
    descent: FlightWaypoint
    land: FlightWaypoint

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        return [
            self.takeoff,
            self.ascent,
            self.hold,
            self.join,
            self.ingress
        ] + self.targets + [
            self.egress,
            self.split,
            self.descent,
            self.land,
        ]

    @property
    def package_speed_waypoints(self) -> Set[FlightWaypoint]:
        return {
            self.ingress,
            self.egress,
            self.split,
        } | set(self.targets)

    @property
    def tot_waypoint(self) -> Optional[FlightWaypoint]:
        return self.targets[0]

    @property
    def mission_speed(self) -> int:
        return GroundSpeed.for_flight(self.flight, self.ingress.alt)


@dataclass(frozen=True)
class CustomFlightPlan(FlightPlan):
    custom_waypoints: List[FlightWaypoint]

    @property
    def waypoints(self) -> List[FlightWaypoint]:
        return self.custom_waypoints

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

        try:
            flight_plan = self.generate_flight_plan(flight, custom_targets)
        except PlanningError:
            logging.exception(f"Could not create flight plan")
            return
        flight.flight_plan = flight_plan

    def generate_flight_plan(
            self, flight: Flight,
            custom_targets: Optional[List[Unit]]) -> FlightPlan:
        # TODO: Flesh out mission types.
        task = flight.flight_type
        if task == FlightType.BARCAP:
            return self.generate_barcap(flight)
        elif task == FlightType.CAS:
            return self.generate_cas(flight)
        elif task == FlightType.DEAD:
            return self.generate_sead(flight, custom_targets)
        elif task == FlightType.ESCORT:
            return self.generate_escort(flight)
        elif task == FlightType.SEAD:
            return self.generate_sead(flight, custom_targets)
        elif task == FlightType.STRIKE:
            return self.generate_strike(flight)
        elif task == FlightType.TARCAP:
            return self.generate_frontline_cap(flight)
        elif task == FlightType.TROOP_TRANSPORT:
            logging.error(
                "Troop transport flight plan generation not implemented"
            )
        raise PlanningError(
            f"{task.name} flight plan generation not implemented")

    def regenerate_package_waypoints(self) -> None:
        ingress_point = self._ingress_point()
        egress_point = self._egress_point()
        join_point = self._join_point(ingress_point)
        split_point = self._split_point(egress_point)

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

    def generate_barcap(self, flight: Flight) -> BarCapFlightPlan:
        """Generate a BARCAP flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        patrol_alt = random.randint(
            self.doctrine.min_patrol_altitude,
            self.doctrine.max_patrol_altitude
        )

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

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        start, end = builder.race_track(start, end, patrol_alt)
        descent, land = builder.rtb(flight.from_cp)

        return BarCapFlightPlan(
            package=self.package,
            flight=flight,
            patrol_duration=self.doctrine.cap_duration,
            takeoff=builder.takeoff(flight.from_cp),
            ascent=builder.ascent(flight.from_cp),
            patrol_start=start,
            patrol_end=end,
            descent=descent,
            land=land
        )

    def generate_frontline_cap(self, flight: Flight) -> FrontLineCapFlightPlan:
        """Generate a CAP flight plan for the given front line.

        Args:
            flight: The flight to generate the flight plan for.
        """
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        ally_cp, enemy_cp = location.control_points
        patrol_alt = random.randint(self.doctrine.min_patrol_altitude,
                                    self.doctrine.max_patrol_altitude)

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

        # Create points
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)

        start, end = builder.race_track(orbit0p, orbit1p, patrol_alt)
        descent, land = builder.rtb(flight.from_cp)
        return FrontLineCapFlightPlan(
            package=self.package,
            flight=flight,
            # Note that this duration only has an effect if there are no
            # flights in the package that have requested escort. If the package
            # requests an escort the CAP flight will remain on station for the
            # duration of the escorted mission, or until it is winchester/bingo.
            patrol_duration=self.doctrine.cap_duration,
            takeoff=builder.takeoff(flight.from_cp),
            ascent=builder.ascent(flight.from_cp),
            patrol_start=start,
            patrol_end=end,
            descent=descent,
            land=land
        )

    def generate_sead(self, flight: Flight,
                      custom_targets: Optional[List[Unit]]) -> StrikeFlightPlan:
        """Generate a SEAD/DEAD flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            custom_targets: Specific radar equipped units selected by the user.
        """
        location = self.package.target

        if not isinstance(location, TheaterGroundObject):
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

    def generate_escort(self, flight: Flight) -> StrikeFlightPlan:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        ingress, target, egress = builder.escort(
            self.package.waypoints.ingress, self.package.target,
            self.package.waypoints.egress)
        descent, land = builder.rtb(flight.from_cp)

        return StrikeFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.from_cp),
            ascent=builder.ascent(flight.from_cp),
            hold=builder.hold(self._hold_point(flight)),
            join=builder.join(self.package.waypoints.join),
            ingress=ingress,
            targets=[target],
            egress=egress,
            split=builder.split(self.package.waypoints.split),
            descent=descent,
            land=land
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
        descent, land = builder.rtb(flight.from_cp)

        return CasFlightPlan(
            package=self.package,
            flight=flight,
            patrol_duration=self.doctrine.cas_duration,
            takeoff=builder.takeoff(flight.from_cp),
            ascent=builder.ascent(flight.from_cp),
            patrol_start=builder.ingress_cas(ingress, location),
            target=builder.cas(center),
            patrol_end=builder.egress(egress, location),
            descent=descent,
            land=land
        )

    @staticmethod
    def target_waypoint(flight: Flight, builder: WaypointBuilder,
                        target: StrikeTarget) -> FlightWaypoint:
        if flight.flight_type == FlightType.DEAD:
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
        heading = flight.from_cp.position.heading_between_point(
            self.package.target.position
        )
        return flight.from_cp.position.point_from_heading(
            heading, nm_to_meter(15)
        )

    # TODO: Make a model for the waypoint builder and use that in the UI.
    def generate_ascend_point(self, flight: Flight,
                              departure: ControlPoint) -> FlightWaypoint:
        """Generate ascend point.

        Args:
            flight: The flight to generate the descend point for.
            departure: Departure airfield or carrier.
        """
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        return builder.ascent(departure)

    def generate_descend_point(self, flight: Flight,
                               arrival: ControlPoint) -> FlightWaypoint:
        """Generate approach/descend point.

        Args:
            flight: The flight to generate the descend point for.
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        return builder.descent(arrival)

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
            self, flight: Flight, location: TheaterGroundObject,
            targets: Optional[List[StrikeTarget]] = None) -> StrikeFlightPlan:
        assert self.package.waypoints is not None
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine,
                                  targets)
        sead_types = {FlightType.DEAD, FlightType.SEAD}
        if flight.flight_type in sead_types:
            ingress = builder.ingress_sead(self.package.waypoints.ingress,
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

        descent, land = builder.rtb(flight.from_cp)
        return StrikeFlightPlan(
            package=self.package,
            flight=flight,
            takeoff=builder.takeoff(flight.from_cp),
            ascent=builder.ascent(flight.from_cp),
            hold=builder.hold(self._hold_point(flight)),
            join=builder.join(self.package.waypoints.join),
            ingress=ingress,
            targets=target_waypoints,
            egress=builder.egress(self.package.waypoints.egress, location),
            split=builder.split(self.package.waypoints.split),
            descent=descent,
            land=land
        )

    def _join_point(self, ingress_point: Point) -> Point:
        heading = self._heading_to_package_airfield(ingress_point)
        return ingress_point.point_from_heading(heading,
                                                -self.doctrine.join_distance)

    def _split_point(self, egress_point: Point) -> Point:
        heading = self._heading_to_package_airfield(egress_point)
        return egress_point.point_from_heading(heading,
                                               -self.doctrine.split_distance)

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
                if flight.from_cp == airfield:
                    return airfield
        raise RuntimeError(
            "Could not find any airfield assigned to this package"
        )
