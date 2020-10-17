"""Flight plan generation.

Flights are first planned generically by either the player or by the
MissionPlanner. Those only plan basic information like the objective, aircraft
type, and the size of the flight. The FlightPlanBuilder is responsible for
generating the waypoints for the mission.
"""
from __future__ import annotations

import logging
import random
from typing import List, Optional, TYPE_CHECKING

from dcs.mapping import Point
from dcs.unit import Unit

from game.data.doctrine import Doctrine, MODERN_DOCTRINE
from game.utils import nm_to_meter
from gen.ato import Package, PackageWaypoints
from theater import ControlPoint, FrontLine, MissionTarget, TheaterGroundObject
from .closestairfields import ObjectiveDistanceCache
from .flight import Flight, FlightType, FlightWaypoint
from .waypointbuilder import WaypointBuilder
from ..conflictgen import Conflict

if TYPE_CHECKING:
    from game import Game


class InvalidObjectiveLocation(RuntimeError):
    """Raised when the objective location is invalid for the mission type."""
    def __init__(self, task: FlightType, location: MissionTarget) -> None:
        super().__init__(
            f"{location.name} is not valid for {task.name} missions."
        )


class FlightPlanBuilder:
    """Generates flight plans for flights."""

    def __init__(self, game: Game, package: Package, is_player: bool) -> None:
        self.game = game
        self.package = package
        self.is_player = is_player
        if is_player:
            faction = self.game.player_faction
        else:
            faction = self.game.enemy_faction
        self.doctrine: Doctrine = faction.get("doctrine", MODERN_DOCTRINE)

    def populate_flight_plan(
            self, flight: Flight,
            # TODO: Custom targets should be an attribute of the flight.
            custom_targets: Optional[List[Unit]] = None) -> None:
        """Creates a default flight plan for the given mission."""
        if flight not in self.package.flights:
            raise RuntimeError("Flight must be a part of the package")
        if self.package.waypoints is None:
            self.regenerate_package_waypoints()

        # TODO: Flesh out mission types.
        try:
            task = flight.flight_type
            if task == FlightType.ANTISHIP:
                logging.error(
                    "Anti-ship flight plan generation not implemented"
                )
            elif task == FlightType.BAI:
                logging.error("BAI flight plan generation not implemented")
            elif task == FlightType.BARCAP:
                self.generate_barcap(flight)
            elif task == FlightType.CAS:
                self.generate_cas(flight)
            elif task == FlightType.DEAD:
                self.generate_sead(flight, custom_targets)
            elif task == FlightType.ELINT:
                logging.error("ELINT flight plan generation not implemented")
            elif task == FlightType.ESCORT:
                self.generate_escort(flight)
            elif task == FlightType.EVAC:
                logging.error("Evac flight plan generation not implemented")
            elif task == FlightType.EWAR:
                logging.error("EWar flight plan generation not implemented")
            elif task == FlightType.INTERCEPTION:
                logging.error(
                    "Intercept flight plan generation not implemented"
                )
            elif task == FlightType.LOGISTICS:
                logging.error(
                    "Logistics flight plan generation not implemented"
                )
            elif task == FlightType.RECON:
                logging.error("Recon flight plan generation not implemented")
            elif task == FlightType.SEAD:
                self.generate_sead(flight, custom_targets)
            elif task == FlightType.STRIKE:
                self.generate_strike(flight)
            elif task == FlightType.TARCAP:
                self.generate_frontline_cap(flight)
            elif task == FlightType.TROOP_TRANSPORT:
                logging.error(
                    "Troop transport flight plan generation not implemented"
                )
            else:
                logging.error(f"Unsupported task type: {task.name}")
        except InvalidObjectiveLocation:
            logging.exception(f"Could not create flight plan")

    def regenerate_package_waypoints(self) -> None:
        ingress_point = self._ingress_point()
        egress_point = self._egress_point()
        join_point = self._join_point(ingress_point)
        split_point = self._split_point(egress_point)

        self.package.waypoints = PackageWaypoints(
            join_point,
            ingress_point,
            egress_point,
            split_point,
        )

    def generate_strike(self, flight: Flight) -> None:
        """Generates a strike flight plan.

        Args:
            flight: The flight to generate the flight plan for.
        """
        assert self.package.waypoints is not None
        location = self.package.target

        # TODO: Support airfield strikes.
        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.ascent(flight.from_cp)
        builder.hold(self._hold_point(flight))
        builder.join(self.package.waypoints.join)
        builder.ingress_strike(self.package.waypoints.ingress, location)

        if len(location.groups) > 0 and location.dcs_identifier == "AA":
            # TODO: Replace with DEAD?
            # Strike missions on SEAD targets target units.
            for g in location.groups:
                for j, u in enumerate(g.units):
                    builder.strike_point(u, f"{u.type} #{j}", location)
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

                builder.strike_point(
                    building,
                    f"{building.obj_name} {building.category}",
                    location
                )

        builder.egress(self.package.waypoints.egress, location)
        builder.split(self.package.waypoints.split)
        builder.rtb(flight.from_cp)

        flight.points = builder.build()

    def generate_barcap(self, flight: Flight) -> None:
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
            logging.error("Could not find any enemy airfields")
            return

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
        builder.ascent(flight.from_cp)
        builder.race_track(start, end, patrol_alt)
        builder.rtb(flight.from_cp)
        flight.points = builder.build()

    def generate_frontline_cap(self, flight: Flight) -> None:
        """Generate a CAP flight plan for the given front line.

        Args:
            flight: The flight to generate the flight plan for.
        """
        assert self.package.waypoints is not None
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
        builder.ascent(flight.from_cp)
        builder.hold(self._hold_point(flight))
        builder.join(self.package.waypoints.join)
        builder.race_track(orbit0p, orbit1p, patrol_alt)
        builder.split(self.package.waypoints.split)
        builder.rtb(flight.from_cp)
        flight.points = builder.build()

    def generate_sead(self, flight: Flight,
                      custom_targets: Optional[List[Unit]]) -> None:
        """Generate a SEAD/DEAD flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            custom_targets: Specific radar equipped units selected by the user.
        """
        assert self.package.waypoints is not None
        location = self.package.target

        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        if custom_targets is None:
            custom_targets = []

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.ascent(flight.from_cp)
        builder.hold(self._hold_point(flight))
        builder.join(self.package.waypoints.join)
        builder.ingress_sead(self.package.waypoints.ingress, location)

        # TODO: Unify these.
        # There doesn't seem to be any reason to treat the UI fragged missions
        # different from the automatic missions.
        if custom_targets:
            for target in custom_targets:
                if flight.flight_type == FlightType.DEAD:
                    builder.dead_point(target, location.name, location)
                else:
                    builder.sead_point(target, location.name, location)
        else:
            if flight.flight_type == FlightType.DEAD:
                builder.dead_area(location)
            else:
                builder.sead_area(location)

        builder.egress(self.package.waypoints.egress, location)
        builder.split(self.package.waypoints.split)
        builder.rtb(flight.from_cp)

        flight.points = builder.build()

    def _hold_point(self, flight: Flight) -> Point:
        heading = flight.from_cp.position.heading_between_point(
            self.package.target.position
        )
        return flight.from_cp.position.point_from_heading(
            heading, nm_to_meter(15)
        )

    def generate_escort(self, flight: Flight) -> None:
        assert self.package.waypoints is not None

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.ascent(flight.from_cp)
        builder.hold(self._hold_point(flight))
        builder.join(self.package.waypoints.join)
        builder.escort(self.package.waypoints.ingress,
                       self.package.target, self.package.waypoints.egress)
        builder.split(self.package.waypoints.split)
        builder.rtb(flight.from_cp)

        flight.points = builder.build()

    def generate_cas(self, flight: Flight) -> None:
        """Generate a CAS flight plan for the given target.

        Args:
            flight: The flight to generate the flight plan for.
        """
        assert self.package.waypoints is not None
        location = self.package.target

        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        is_helo = getattr(flight.unit_type, "helicopter", False)
        cap_alt = 500 if is_helo else 1000

        ingress, heading, distance = Conflict.frontline_vector(
            location.control_points[0], location.control_points[1],
            self.game.theater
        )
        center = ingress.point_from_heading(heading, distance / 2)
        egress = ingress.point_from_heading(heading, distance)

        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.ascent(flight.from_cp, is_helo)
        builder.hold(self._hold_point(flight))
        builder.join(self.package.waypoints.join)
        builder.ingress_cas(ingress, location)
        builder.cas(center, cap_alt)
        builder.egress(egress, location)
        builder.split(self.package.waypoints.split)
        builder.rtb(flight.from_cp, is_helo)

        flight.points = builder.build()

    # TODO: Make a model for the waypoint builder and use that in the UI.
    def generate_ascend_point(self, flight: Flight,
                              departure: ControlPoint) -> FlightWaypoint:
        """Generate ascend point.

        Args:
            flight: The flight to generate the descend point for.
            departure: Departure airfield or carrier.
        """
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.ascent(departure)
        return builder.build()[0]

    def generate_descend_point(self, flight: Flight,
                               arrival: ControlPoint) -> FlightWaypoint:
        """Generate approach/descend point.

        Args:
            flight: The flight to generate the descend point for.
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.descent(arrival)
        return builder.build()[0]

    def generate_rtb_waypoint(self, flight: Flight,
                              arrival: ControlPoint) -> FlightWaypoint:
        """Generate RTB landing point.

        Args:
            flight: The flight to generate the landing waypoint for.
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(self.game.conditions, flight, self.doctrine)
        builder.land(arrival)
        return builder.build()[0]

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
