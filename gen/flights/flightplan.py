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

from dcs.unit import Unit

from game.data.doctrine import Doctrine, MODERN_DOCTRINE
from game.utils import nm_to_meter
from theater import ControlPoint, FrontLine, MissionTarget, TheaterGroundObject
from .closestairfields import ObjectiveDistanceCache
from .flight import Flight, FlightType, FlightWaypoint, FlightWaypointType
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

    def __init__(self, game: Game, is_player: bool) -> None:
        self.game = game
        self.is_player = is_player
        if is_player:
            faction = self.game.player_faction
        else:
            faction = self.game.enemy_faction
        self.doctrine: Doctrine = faction.get("doctrine", MODERN_DOCTRINE)

    def populate_flight_plan(self, flight: Flight,
                             objective_location: MissionTarget) -> None:
        """Creates a default flight plan for the given mission."""
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
                self.generate_barcap(flight, objective_location)
            elif task == FlightType.CAP:
                self.generate_barcap(flight, objective_location)
            elif task == FlightType.CAS:
                self.generate_cas(flight, objective_location)
            elif task == FlightType.DEAD:
                self.generate_sead(flight, objective_location)
            elif task == FlightType.ELINT:
                logging.error("ELINT flight plan generation not implemented")
            elif task == FlightType.ESCORT:
                self.generate_escort(flight, objective_location)
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
                self.generate_sead(flight, objective_location)
            elif task == FlightType.STRIKE:
                self.generate_strike(flight, objective_location)
            elif task == FlightType.TARCAP:
                self.generate_frontline_cap(flight, objective_location)
            elif task == FlightType.TROOP_TRANSPORT:
                logging.error(
                    "Troop transport flight plan generation not implemented"
                )
        except InvalidObjectiveLocation as ex:
            logging.error(f"Could not create flight plan: {ex}")

    def generate_strike(self, flight: Flight, location: MissionTarget) -> None:
        """Generates a strike flight plan.

        Args:
            flight: The flight to generate the flight plan for.
            location: The strike target location.
        """
        # TODO: Support airfield strikes.
        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        # TODO: Stop clobbering flight type.
        flight.flight_type = FlightType.STRIKE

        heading = flight.from_cp.position.heading_between_point(
            location.position
        )
        ingress_heading = heading - 180 + 25

        ingress_pos = location.position.point_from_heading(
            ingress_heading, self.doctrine.ingress_egress_distance
        )

        egress_heading = heading - 180 - 25
        egress_pos = location.position.point_from_heading(
            egress_heading, self.doctrine.ingress_egress_distance
        )

        builder = WaypointBuilder(self.doctrine)
        builder.ascent(flight.from_cp)
        builder.ingress_strike(ingress_pos, location)

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

        builder.egress(egress_pos, location)
        builder.rtb(flight.from_cp)

        flight.points = builder.build()

    def generate_barcap(self, flight: Flight, location: MissionTarget) -> None:
        """Generate a BARCAP flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            location: The control point to protect.
        """
        if isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        if isinstance(location, ControlPoint) and location.is_carrier:
            flight.flight_type = FlightType.BARCAP
        else:
            flight.flight_type = FlightType.CAP

        patrol_alt = random.randint(
            self.doctrine.min_patrol_altitude,
            self.doctrine.max_patrol_altitude
        )

        closest_cache = ObjectiveDistanceCache.get_closest_airfields(location)
        for airfield in closest_cache.closest_airfields:
            if airfield.captured != self.is_player:
                closest_airfield = airfield
                break
        else:
            logging.error("Could not find any enemy airfields")
            return

        heading = location.position.heading_between_point(
            closest_airfield.position
        )

        end = location.position.point_from_heading(
            heading,
            random.randint(self.doctrine.cap_min_distance_from_cp,
                           self.doctrine.cap_max_distance_from_cp)
        )
        diameter = random.randint(
            self.doctrine.cap_min_track_length,
            self.doctrine.cap_max_track_length
        )
        start = end.point_from_heading(heading - 180, diameter)

        builder = WaypointBuilder(self.doctrine)
        builder.ascent(flight.from_cp)
        builder.race_track(start, end, patrol_alt)
        builder.rtb(flight.from_cp)
        flight.points = builder.build()

    def generate_frontline_cap(self, flight: Flight,
                               location: MissionTarget) -> None:
        """Generate a CAP flight plan for the given front line.

        Args:
            flight: The flight to generate the flight plan for.
            location: Front line to protect.
        """
        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        ally_cp, enemy_cp = location.control_points
        flight.flight_type = FlightType.CAP
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
        builder = WaypointBuilder(self.doctrine)
        builder.ascent(flight.from_cp)
        builder.race_track(orbit0p, orbit1p, patrol_alt)
        builder.rtb(flight.from_cp)
        flight.points = builder.build()

    def generate_sead(self, flight: Flight, location: MissionTarget,
                      custom_targets: Optional[List[Unit]] = None) -> None:
        """Generate a SEAD/DEAD flight at a given location.

        Args:
            flight: The flight to generate the flight plan for.
            location: Location of the SAM site.
            custom_targets: Specific radar equipped units selected by the user.
        """
        if not isinstance(location, TheaterGroundObject):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        if custom_targets is None:
            custom_targets = []

        flight.flight_type = random.choice([FlightType.SEAD, FlightType.DEAD])

        heading = flight.from_cp.position.heading_between_point(
            location.position
        )
        ingress_heading = heading - 180 + 25

        ingress_pos = location.position.point_from_heading(
            ingress_heading, self.doctrine.ingress_egress_distance
        )

        egress_heading = heading - 180 - 25
        egress_pos = location.position.point_from_heading(
            egress_heading, self.doctrine.ingress_egress_distance
        )

        builder = WaypointBuilder(self.doctrine)
        builder.ascent(flight.from_cp)
        builder.ingress_sead(ingress_pos, location)

        # TODO: Unify these.
        # There doesn't seem to be any reason to treat the UI fragged missions
        # different from the automatic missions.
        if custom_targets:
            for target in custom_targets:
                point = FlightWaypoint(
                    FlightWaypointType.TARGET_POINT,
                    target.position.x,
                    target.position.y,
                    0
                )
                point.alt_type = "RADIO"
                if flight.flight_type == FlightType.DEAD:
                    builder.dead_point(target, location.name, location)
                else:
                    builder.sead_point(target, location.name, location)
        else:
            if flight.flight_type == FlightType.DEAD:
                builder.dead_area(location)
            else:
                builder.sead_area(location)

        builder.egress(egress_pos, location)
        builder.rtb(flight.from_cp)

        flight.points = builder.build()

    def generate_escort(self, flight: Flight, location: MissionTarget) -> None:
        flight.flight_type = FlightType.ESCORT

        # TODO: Decide common waypoints for the package ahead of time.
        # Packages should determine some common points like push, ingress,
        # egress, and split points ahead of time so they can be shared by all
        # flights.
        heading = flight.from_cp.position.heading_between_point(
            location.position
        )
        ingress_heading = heading - 180 + 25

        ingress_pos = location.position.point_from_heading(
            ingress_heading, self.doctrine.ingress_egress_distance
        )

        egress_heading = heading - 180 - 25
        egress_pos = location.position.point_from_heading(
            egress_heading, self.doctrine.ingress_egress_distance
        )

        patrol_alt = random.randint(
            self.doctrine.min_patrol_altitude,
            self.doctrine.max_patrol_altitude
        )

        builder = WaypointBuilder(self.doctrine)
        builder.ascent(flight.from_cp)
        builder.race_track(ingress_pos, egress_pos, patrol_alt)
        builder.rtb(flight.from_cp)

        flight.points = builder.build()

    def generate_cas(self, flight: Flight, location: MissionTarget) -> None:
        """Generate a CAS flight plan for the given target.

        Args:
            flight: The flight to generate the flight plan for.
            location: Front line with CAS targets.
        """
        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        is_helo = getattr(flight.unit_type, "helicopter", False)
        cap_alt = 500 if is_helo else 1000
        flight.flight_type = FlightType.CAS

        ingress, heading, distance = Conflict.frontline_vector(
            location.control_points[0], location.control_points[1],
            self.game.theater
        )
        center = ingress.point_from_heading(heading, distance / 2)
        egress = ingress.point_from_heading(heading, distance)

        builder = WaypointBuilder(self.doctrine)
        builder.ascent(flight.from_cp, is_helo)
        builder.ingress_cas(ingress, location)
        builder.cas(center, cap_alt)
        builder.egress(egress, location)
        builder.rtb(flight.from_cp, is_helo)

        flight.points = builder.build()

    # TODO: Make a model for the waypoint builder and use that in the UI.
    def generate_ascend_point(self, departure: ControlPoint) -> FlightWaypoint:
        """Generate ascend point.

        Args:
            departure: Departure airfield or carrier.
        """
        builder = WaypointBuilder(self.doctrine)
        builder.ascent(departure)
        return builder.build()[0]

    def generate_descend_point(self, arrival: ControlPoint) -> FlightWaypoint:
        """Generate approach/descend point.

        Args:
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(self.doctrine)
        builder.descent(arrival)
        return builder.build()[0]

    @staticmethod
    def generate_rtb_waypoint(arrival: ControlPoint) -> FlightWaypoint:
        """Generate RTB landing point.

        Args:
            arrival: Arrival airfield or carrier.
        """
        builder = WaypointBuilder(self.doctrine)
        builder.land(arrival)
        return builder.build()[0]
