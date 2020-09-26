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

from game.data.doctrine import MODERN_DOCTRINE
from .flight import Flight, FlightType, FlightWaypointType, FlightWaypoint
from ..conflictgen import Conflict
from theater import ControlPoint, FrontLine, MissionTarget, TheaterGroundObject
from game.utils import nm_to_meter
from dcs.unit import Unit

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
        if is_player:
            faction = self.game.player_faction
        else:
            faction = self.game.enemy_faction
        self.doctrine = faction.get("doctrine", MODERN_DOCTRINE)

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
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        heading = flight.from_cp.position.heading_between_point(
            location.position
        )
        ingress_heading = heading - 180 + 25
        egress_heading = heading - 180 - 25

        ingress_pos = location.position.point_from_heading(
            ingress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"]
        )
        ingress_point = FlightWaypoint(
            FlightWaypointType.INGRESS_STRIKE,
            ingress_pos.x,
            ingress_pos.y,
            self.doctrine["INGRESS_ALT"]
        )
        ingress_point.pretty_name = "INGRESS on " + location.name
        ingress_point.description = "INGRESS on " + location.name
        ingress_point.name = "INGRESS"
        flight.points.append(ingress_point)

        if len(location.groups) > 0 and location.dcs_identifier == "AA":
            for g in location.groups:
                for j, u in enumerate(g.units):
                    point = FlightWaypoint(
                        FlightWaypointType.TARGET_POINT,
                        u.position.x,
                        u.position.y,
                        0
                    )
                    point.description = (
                        f"STRIKE [{location.name}] : {u.type} #{j}"
                    )
                    point.pretty_name = (
                        f"STRIKE [{location.name}] : {u.type} #{j}"
                    )
                    point.name = f"{location.name} #{j}"
                    point.only_for_player = True
                    ingress_point.targets.append(location)
                    flight.points.append(point)
        else:
            if hasattr(location, "obj_name"):
                buildings = self.game.theater.find_ground_objects_by_obj_name(
                    location.obj_name
                )
                for building in buildings:
                    if building.is_dead:
                        continue

                    point = FlightWaypoint(
                        FlightWaypointType.TARGET_POINT,
                        building.position.x,
                        building.position.y,
                        0
                    )
                    point.description = (
                        f"STRIKE on {building.obj_name} {building.category} "
                        f"[{building.dcs_identifier}]"
                    )
                    point.pretty_name = (
                        f"STRIKE on {building.obj_name} {building.category} "
                        f"[{building.dcs_identifier}]"
                    )
                    point.name = building.obj_name
                    point.only_for_player = True
                    ingress_point.targets.append(building)
                    flight.points.append(point)
            else:
                point = FlightWaypoint(
                    FlightWaypointType.TARGET_GROUP_LOC,
                    location.position.x,
                    location.position.y,
                    0
                )
                point.description = "STRIKE on " + location.name
                point.pretty_name = "STRIKE on " + location.name
                point.name = location.name
                point.only_for_player = True
                ingress_point.targets.append(location)
                flight.points.append(point)

        egress_pos = location.position.point_from_heading(
            egress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"]
        )
        egress_point = FlightWaypoint(
            FlightWaypointType.EGRESS,
            egress_pos.x,
            egress_pos.y,
            self.doctrine["EGRESS_ALT"]
        )
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS from " + location.name
        egress_point.description = "EGRESS from " + location.name
        flight.points.append(egress_point)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)

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
            self.doctrine["PATROL_ALT_RANGE"][0],
            self.doctrine["PATROL_ALT_RANGE"][1]
        )

        loc = location.position.point_from_heading(
            random.randint(0, 360),
            random.randint(self.doctrine["CAP_DISTANCE_FROM_CP"][0],
                           self.doctrine["CAP_DISTANCE_FROM_CP"][1])
        )
        hdg = location.position.heading_between_point(loc)
        radius = random.randint(
            self.doctrine["CAP_PATTERN_LENGTH"][0],
            self.doctrine["CAP_PATTERN_LENGTH"][1]
        )
        orbit0p = loc.point_from_heading(hdg - 90, radius)
        orbit1p = loc.point_from_heading(hdg + 90, radius)

        # Create points
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        orbit0 = FlightWaypoint(
            FlightWaypointType.PATROL_TRACK,
            orbit0p.x,
            orbit0p.y,
            patrol_alt
        )
        orbit0.name = "ORBIT 0"
        orbit0.description = "Standby between this point and the next one"
        orbit0.pretty_name = "Race-track start"
        flight.points.append(orbit0)

        orbit1 = FlightWaypoint(
            FlightWaypointType.PATROL,
            orbit1p.x,
            orbit1p.y,
            patrol_alt
        )
        orbit1.name = "ORBIT 1"
        orbit1.description = "Standby between this point and the previous one"
        orbit1.pretty_name = "Race-track end"
        flight.points.append(orbit1)

        orbit0.targets.append(location)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)

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
        patrol_alt = random.randint(self.doctrine["PATROL_ALT_RANGE"][0],
                                    self.doctrine["PATROL_ALT_RANGE"][1])

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
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        orbit0 = FlightWaypoint(
            FlightWaypointType.PATROL_TRACK,
            orbit0p.x,
            orbit0p.y,
            patrol_alt
        )
        orbit0.name = "ORBIT 0"
        orbit0.description = "Standby between this point and the next one"
        orbit0.pretty_name = "Race-track start"
        flight.points.append(orbit0)

        orbit1 = FlightWaypoint(
            FlightWaypointType.PATROL,
            orbit1p.x,
            orbit1p.y,
            patrol_alt
        )
        orbit1.name = "ORBIT 1"
        orbit1.description = "Standby between this point and the previous one"
        orbit1.pretty_name = "Race-track end"
        flight.points.append(orbit1)

        # Note: Targets of PATROL TRACK waypoints are the points to be defended.
        orbit0.targets.append(flight.from_cp)
        orbit0.targets.append(center)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)

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

        flight.points = []
        flight.flight_type = random.choice([FlightType.SEAD, FlightType.DEAD])

        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        heading = flight.from_cp.position.heading_between_point(
            location.position
        )
        ingress_heading = heading - 180 + 25
        egress_heading = heading - 180 - 25

        ingress_pos = location.position.point_from_heading(
            ingress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"]
        )
        ingress_point = FlightWaypoint(
            FlightWaypointType.INGRESS_SEAD,
            ingress_pos.x,
            ingress_pos.y,
            self.doctrine["INGRESS_ALT"]
        )
        ingress_point.name = "INGRESS"
        ingress_point.pretty_name = "INGRESS on " + location.name
        ingress_point.description = "INGRESS on " + location.name
        flight.points.append(ingress_point)

        if len(custom_targets) > 0:
            for target in custom_targets:
                point = FlightWaypoint(
                    FlightWaypointType.TARGET_POINT,
                    target.position.x,
                    target.position.y,
                    0
                )
                point.alt_type = "RADIO"
                if flight.flight_type == FlightType.DEAD:
                    point.description = "DEAD on " + target.type
                    point.pretty_name = "DEAD on " + location.name
                    point.only_for_player = True
                else:
                    point.description = "SEAD on " + location.name
                    point.pretty_name = "SEAD on " + location.name
                    point.only_for_player = True
                flight.points.append(point)
            ingress_point.targets.append(location)
            ingress_point.targetGroup = location
        else:
            point = FlightWaypoint(
                FlightWaypointType.TARGET_GROUP_LOC,
                location.position.x,
                location.position.y,
                0
            )
            point.alt_type = "RADIO"
            if flight.flight_type == FlightType.DEAD:
                point.description = "DEAD on " + location.name
                point.pretty_name = "DEAD on " + location.name
                point.only_for_player = True
            else:
                point.description = "SEAD on " + location.name
                point.pretty_name = "SEAD on " + location.name
                point.only_for_player = True
            ingress_point.targets.append(location)
            ingress_point.targetGroup = location
            flight.points.append(point)

        egress_pos = location.position.point_from_heading(
            egress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"]
        )
        egress_point = FlightWaypoint(
            FlightWaypointType.EGRESS,
            egress_pos.x,
            egress_pos.y,
            self.doctrine["EGRESS_ALT"]
        )
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS from " + location.name
        egress_point.description = "EGRESS from " + location.name
        flight.points.append(egress_point)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)

    def generate_cas(self, flight: Flight, location: MissionTarget) -> None:
        """Generate a CAS flight plan for the given target.

        Args:
            flight: The flight to generate the flight plan for.
            location: Front line with CAS targets.
        """
        if not isinstance(location, FrontLine):
            raise InvalidObjectiveLocation(flight.flight_type, location)

        from_cp, location = location.control_points
        is_helo = getattr(flight.unit_type, "helicopter", False)
        cap_alt = 1000
        flight.points = []
        flight.flight_type = FlightType.CAS

        ingress, heading, distance = Conflict.frontline_vector(
            from_cp, location, self.game.theater
        )
        center = ingress.point_from_heading(heading, distance / 2)
        egress = ingress.point_from_heading(heading, distance)

        ascend = self.generate_ascend_point(flight.from_cp)
        if is_helo:
            cap_alt = 500
            ascend.alt = 500
        flight.points.append(ascend)

        ingress_point = FlightWaypoint(
            FlightWaypointType.INGRESS_CAS,
            ingress.x,
            ingress.y,
            cap_alt
        )
        ingress_point.alt_type = "RADIO"
        ingress_point.name = "INGRESS"
        ingress_point.pretty_name = "INGRESS"
        ingress_point.description = "Ingress into CAS area"
        flight.points.append(ingress_point)

        center_point = FlightWaypoint(
            FlightWaypointType.CAS,
            center.x,
            center.y,
            cap_alt
        )
        center_point.alt_type = "RADIO"
        center_point.description = "Provide CAS"
        center_point.name = "CAS"
        center_point.pretty_name = "CAS"
        flight.points.append(center_point)

        egress_point = FlightWaypoint(
            FlightWaypointType.EGRESS,
            egress.x,
            egress.y,
            cap_alt
        )
        egress_point.alt_type = "RADIO"
        egress_point.description = "Egress from CAS area"
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS"
        flight.points.append(egress_point)

        descend = self.generate_descend_point(flight.from_cp)
        if is_helo:
            descend.alt = 300
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)

    def generate_ascend_point(self, departure: ControlPoint) -> FlightWaypoint:
        """Generate ascend point.

        Args:
            departure: Departure airfield or carrier.
        """
        ascend_heading = departure.heading
        pos_ascend = departure.position.point_from_heading(
            ascend_heading, 10000
        )
        ascend = FlightWaypoint(
            FlightWaypointType.ASCEND_POINT,
            pos_ascend.x,
            pos_ascend.y,
            self.doctrine["PATTERN_ALTITUDE"]
        )
        ascend.name = "ASCEND"
        ascend.alt_type = "RADIO"
        ascend.description = "Ascend"
        ascend.pretty_name = "Ascend"
        return ascend

    def generate_descend_point(self, arrival: ControlPoint) -> FlightWaypoint:
        """Generate approach/descend point.

        Args:
            arrival: Arrival airfield or carrier.
        """
        ascend_heading = arrival.heading
        descend = arrival.position.point_from_heading(
            ascend_heading - 180, 10000
        )
        descend = FlightWaypoint(
            FlightWaypointType.DESCENT_POINT,
            descend.x,
            descend.y,
            self.doctrine["PATTERN_ALTITUDE"]
        )
        descend.name = "DESCEND"
        descend.alt_type = "RADIO"
        descend.description = "Descend to pattern alt"
        descend.pretty_name = "Descend to pattern alt"
        return descend

    @staticmethod
    def generate_rtb_waypoint(arrival: ControlPoint) -> FlightWaypoint:
        """Generate RTB landing point.

        Args:
            arrival: Arrival airfield or carrier.
        """
        rtb = arrival.position
        rtb = FlightWaypoint(
            FlightWaypointType.LANDING_POINT,
            rtb.x,
            rtb.y,
            0
        )
        rtb.name = "LANDING"
        rtb.alt_type = "RADIO"
        rtb.description = "RTB"
        rtb.pretty_name = "RTB"
        return rtb
