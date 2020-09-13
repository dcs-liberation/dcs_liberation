import math
import operator
import random
from typing import Iterable, Iterator, List, Tuple

from dcs.unittype import FlyingType

from game import db
from game.data.doctrine import MODERN_DOCTRINE
from game.data.radar_db import UNITS_WITH_RADAR
from game.utils import nm_to_meter
from gen import Conflict
from gen.ato import Package
from gen.flights.ai_flight_planner_db import (
    CAP_CAPABLE,
    CAS_CAPABLE,
    DRONES,
    SEAD_CAPABLE,
    STRIKE_CAPABLE,
)
from gen.flights.flight import (
    Flight,
    FlightType,
    FlightWaypoint,
    FlightWaypointType,
)
from theater.controlpoint import ControlPoint
from theater.missiontarget import MissionTarget
from theater.theatergroundobject import TheaterGroundObject

MISSION_DURATION = 80


# TODO: Should not be per-control point.
# Packages can frag flights from individual airfields, so we should be planning
# coalition wide rather than per airfield.
class FlightPlanner:

    def __init__(self, from_cp: ControlPoint, game: "Game") -> None:
        # TODO : have the flight planner depend on a 'stance' setting : [Defensive, Aggresive... etc] and faction doctrine
        # TODO : the flight planner should plan package and operations
        self.from_cp = from_cp
        self.game = game
        self.flights: List[Flight] = []
        self.potential_sead_targets: List[Tuple[TheaterGroundObject, int]] = []
        self.potential_strike_targets: List[Tuple[TheaterGroundObject, int]] = []

        if from_cp.captured:
            self.faction = self.game.player_faction
        else:
            self.faction = self.game.enemy_faction

        if "doctrine" in self.faction.keys():
            self.doctrine = self.faction["doctrine"]
        else:
            self.doctrine = MODERN_DOCTRINE

    @property
    def aircraft_inventory(self) -> "GlobalAircraftInventory":
        return self.game.aircraft_inventory

    def reset(self) -> None:
        """Reset the planned flights and available units."""
        self.flights = []
        self.potential_sead_targets = []
        self.potential_strike_targets = []

    def plan_flights(self) -> None:
        self.reset()
        self.compute_sead_targets()
        self.compute_strike_targets()

        self.commission_cap()
        self.commission_cas()
        self.commission_sead()
        self.commission_strike()
        # TODO: Commission anti-ship and intercept.

    def plan_legacy_mission(self, flight: Flight,
                            location: MissionTarget) -> None:
        package = Package(location)
        package.add_flight(flight)
        if flight.from_cp.captured:
            self.game.blue_ato.add_package(package)
        else:
            self.game.red_ato.add_package(package)
        self.flights.append(flight)
        self.aircraft_inventory.claim_for_flight(flight)

    def get_compatible_aircraft(self, candidates: Iterable[FlyingType],
                                minimum: int) -> List[FlyingType]:
        inventory = self.aircraft_inventory.for_control_point(self.from_cp)
        return [k for k, v in inventory.all_aircraft if
                k in candidates and v >= minimum]

    def alloc_aircraft(
            self, num_flights: int, flight_size: int,
            allowed_types: Iterable[FlyingType]) -> Iterator[FlyingType]:
        aircraft = self.get_compatible_aircraft(allowed_types, flight_size)
        if not aircraft:
            return

        for _ in range(num_flights):
            yield random.choice(aircraft)
            aircraft = self.get_compatible_aircraft(allowed_types, flight_size)
            if not aircraft:
                return

    def commission_cap(self) -> None:
        """Pick some aircraft to assign them to defensive CAP roles (BARCAP)."""
        offset = random.randint(0, 5)
        num_caps = MISSION_DURATION // self.doctrine["CAP_EVERY_X_MINUTES"]
        for i, aircraft in enumerate(self.alloc_aircraft(num_caps, 2, CAP_CAPABLE)):
            flight = Flight(aircraft, 2, self.from_cp, FlightType.CAP)

            flight.scheduled_in = offset + i * random.randint(
                self.doctrine["CAP_EVERY_X_MINUTES"] - 5,
                self.doctrine["CAP_EVERY_X_MINUTES"] + 5
            )

            if len(self._get_cas_locations()) > 0:
                enemy_cp = random.choice(self._get_cas_locations())
                location = enemy_cp
                self.generate_frontline_cap(flight, flight.from_cp, enemy_cp)
            else:
                location = flight.from_cp
                self.generate_barcap(flight, flight.from_cp)

            self.plan_legacy_mission(flight, location)

    def commission_cas(self) -> None:
        """Pick some aircraft to assign them to CAS."""
        cas_locations = self._get_cas_locations()
        if not cas_locations:
            return

        offset = random.randint(0,5)
        num_cas = MISSION_DURATION // self.doctrine["CAS_EVERY_X_MINUTES"]
        for i, aircraft in enumerate(self.alloc_aircraft(num_cas, 2, CAS_CAPABLE)):
            flight = Flight(aircraft, 2, self.from_cp, FlightType.CAS)
            flight.scheduled_in = offset + i * random.randint(
                self.doctrine["CAS_EVERY_X_MINUTES"] - 5,
                self.doctrine["CAS_EVERY_X_MINUTES"] + 5)
            location = random.choice(cas_locations)

            self.generate_cas(flight, flight.from_cp, location)
            self.plan_legacy_mission(flight, location)

    def commission_sead(self) -> None:
        """Pick some aircraft to assign them to SEAD tasks."""

        if not self.potential_sead_targets:
            return

        offset = random.randint(0, 5)
        num_sead = max(
            MISSION_DURATION // self.doctrine["SEAD_EVERY_X_MINUTES"],
            len(self.potential_sead_targets))
        for i, aircraft in enumerate(self.alloc_aircraft(num_sead, 2, SEAD_CAPABLE)):
            flight = Flight(aircraft, 2, self.from_cp,
                            random.choice([FlightType.SEAD, FlightType.DEAD]))
            flight.scheduled_in = offset + i * random.randint(
                self.doctrine["SEAD_EVERY_X_MINUTES"] - 5,
                self.doctrine["SEAD_EVERY_X_MINUTES"] + 5)

            location = self.potential_sead_targets[0][0]
            self.potential_sead_targets.pop()

            self.generate_sead(flight, location, [])
            self.plan_legacy_mission(flight, location)

    def commission_strike(self) -> None:
        """Pick some aircraft to assign them to STRIKE tasks."""
        if not self.potential_strike_targets:
            return

        offset = random.randint(0,5)
        num_strike = max(
            MISSION_DURATION / self.doctrine["STRIKE_EVERY_X_MINUTES"],
            len(self.potential_strike_targets)
        )
        for i, aircraft in enumerate(self.alloc_aircraft(num_strike, 2, STRIKE_CAPABLE)):
            if aircraft in DRONES:
                count = 1
            else:
                count = 2

            flight = Flight(aircraft, count, self.from_cp, FlightType.STRIKE)
            flight.scheduled_in = offset + i * random.randint(
                self.doctrine["STRIKE_EVERY_X_MINUTES"] - 5,
                self.doctrine["STRIKE_EVERY_X_MINUTES"] + 5)

            location = self.potential_strike_targets[0][0]
            self.potential_strike_targets.pop(0)

            self.generate_strike(flight, location)
            self.plan_legacy_mission(flight, location)

    def _get_cas_locations(self):
        return self._get_cas_locations_for_cp(self.from_cp)

    def _get_cas_locations_for_cp(self, for_cp):
        cas_locations = []
        for cp in for_cp.connected_points:
            if cp.captured != for_cp.captured:
                cas_locations.append(cp)
        return cas_locations

    def compute_strike_targets(self):
        """
        @return a list of potential strike targets in range
        """

        # target, distance
        self.potential_strike_targets = []

        for cp in [c for c in self.game.theater.controlpoints if c.captured != self.from_cp.captured]:

            # Compute distance to current cp
            distance = math.hypot(cp.position.x - self.from_cp.position.x,
                                  cp.position.y - self.from_cp.position.y)

            if distance > 2*self.doctrine["STRIKE_MAX_RANGE"]:
                # Then it's unlikely any child ground object is in range
                return

            added_group = []
            for g in cp.ground_objects:
                if g.group_id in added_group or g.is_dead: continue

                # Compute distance to current cp
                distance = math.hypot(cp.position.x - self.from_cp.position.x,
                                      cp.position.y - self.from_cp.position.y)

                if distance < self.doctrine["SEAD_MAX_RANGE"]:
                    self.potential_strike_targets.append((g, distance))
                    added_group.append(g)

        self.potential_strike_targets.sort(key=operator.itemgetter(1))

    def compute_sead_targets(self):
        """
        @return a list of potential sead targets in range
        """

        # target, distance
        self.potential_sead_targets = []

        for cp in [c for c in self.game.theater.controlpoints if c.captured != self.from_cp.captured]:

            # Compute distance to current cp
            distance = math.hypot(cp.position.x - self.from_cp.position.x,
                                  cp.position.y - self.from_cp.position.y)

            # Then it's unlikely any ground object is range
            if distance > 2*self.doctrine["SEAD_MAX_RANGE"]:
                return

            for g in cp.ground_objects:

                if g.dcs_identifier == "AA":

                    # Check that there is at least one unit with a radar in the ground objects unit groups
                    number_of_units = sum([len([r for r in group.units if db.unit_type_from_name(r.type) in UNITS_WITH_RADAR]) for group in g.groups])
                    if number_of_units <= 0:
                        continue

                    # Compute distance to current cp
                    distance = math.hypot(cp.position.x - self.from_cp.position.x,
                                          cp.position.y - self.from_cp.position.y)

                    if distance < self.doctrine["SEAD_MAX_RANGE"]:
                        self.potential_sead_targets.append((g, distance))

        self.potential_sead_targets.sort(key=operator.itemgetter(1))

    def __repr__(self):
        return "-"*40 + "\n" + self.from_cp.name + " planned flights :\n"\
               + "-"*40 + "\n" + "\n".join([repr(f) for f in self.flights]) + "\n" + "-"*40

    def generate_strike(self, flight: Flight, location: TheaterGroundObject):
        flight.flight_type = FlightType.STRIKE
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        heading = flight.from_cp.position.heading_between_point(location.position)
        ingress_heading = heading - 180 + 25
        egress_heading = heading - 180 - 25

        ingress_pos = location.position.point_from_heading(ingress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"])
        ingress_point = FlightWaypoint(
            FlightWaypointType.INGRESS_STRIKE,
            ingress_pos.x,
            ingress_pos.y,
            self.doctrine["INGRESS_ALT"]
        )
        ingress_point.pretty_name = "INGRESS on " + location.obj_name
        ingress_point.description = "INGRESS on " + location.obj_name
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
                    point.description = "STRIKE " + "[" + str(location.obj_name) + "] : " + u.type + " #" + str(j)
                    point.pretty_name = "STRIKE " + "[" + str(location.obj_name) + "] : " + u.type + " #" + str(j)
                    point.name = location.obj_name + "#" + str(j)
                    point.only_for_player = True
                    ingress_point.targets.append(location)
                    flight.points.append(point)
        else:
            if hasattr(location, "obj_name"):
                buildings = self.game.theater.find_ground_objects_by_obj_name(location.obj_name)
                print(buildings)
                for building in buildings:
                    print("BUILDING " + str(building.is_dead) + " " + str(building.dcs_identifier))
                    if building.is_dead:
                        continue

                    point = FlightWaypoint(
                        FlightWaypointType.TARGET_POINT,
                        building.position.x,
                        building.position.y,
                        0
                    )
                    point.description = "STRIKE on " + building.obj_name + " " + building.category + " [" + str(building.dcs_identifier) + " ]"
                    point.pretty_name = "STRIKE on " + building.obj_name + " " + building.category + " [" + str(building.dcs_identifier) + " ]"
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
                point.description = "STRIKE on " + location.obj_name
                point.pretty_name = "STRIKE on " + location.obj_name
                point.name = location.obj_name
                point.only_for_player = True
                ingress_point.targets.append(location)
                flight.points.append(point)

        egress_pos = location.position.point_from_heading(egress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"])
        egress_point = FlightWaypoint(
            FlightWaypointType.EGRESS,
            egress_pos.x,
            egress_pos.y,
            self.doctrine["EGRESS_ALT"]
        )
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS from " + location.obj_name
        egress_point.description = "EGRESS from " + location.obj_name
        flight.points.append(egress_point)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)

    def generate_barcap(self, flight, for_cp):
        """
        Generate a barcap flight at a given location
        :param flight: Flight to setup
        :param for_cp: CP to protect
        """
        flight.flight_type = FlightType.BARCAP if for_cp.is_carrier else FlightType.CAP
        patrol_alt = random.randint(self.doctrine["PATROL_ALT_RANGE"][0], self.doctrine["PATROL_ALT_RANGE"][1])

        if len(for_cp.ground_objects) > 0:
            loc = random.choice(for_cp.ground_objects)
            hdg = for_cp.position.heading_between_point(loc.position)
            radius = random.randint(self.doctrine["CAP_PATTERN_LENGTH"][0], self.doctrine["CAP_PATTERN_LENGTH"][1])
            orbit0p = loc.position.point_from_heading(hdg - 90, radius)
            orbit1p = loc.position.point_from_heading(hdg + 90, radius)
        else:
            loc = for_cp.position.point_from_heading(random.randint(0, 360), random.randint(self.doctrine["CAP_DISTANCE_FROM_CP"][0], self.doctrine["CAP_DISTANCE_FROM_CP"][1]))
            hdg = for_cp.position.heading_between_point(loc)
            radius = random.randint(self.doctrine["CAP_PATTERN_LENGTH"][0], self.doctrine["CAP_PATTERN_LENGTH"][1])
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

        orbit0.targets.append(for_cp)
        obj_added = []
        for ground_object in for_cp.ground_objects:
            if ground_object.obj_name not in obj_added and not ground_object.airbase_group:
                orbit0.targets.append(ground_object)
                obj_added.append(ground_object.obj_name)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)


    def generate_frontline_cap(self, flight, ally_cp, enemy_cp):
        """
        Generate a cap flight for the frontline between ally_cp and enemy cp in order to ensure air superiority and
        protect friendly CAP airbase
        :param flight: Flight to setup
        :param ally_cp: CP to protect
        :param enemy_cp: Enemy connected cp
        """
        flight.flight_type = FlightType.CAP
        patrol_alt = random.randint(self.doctrine["PATROL_ALT_RANGE"][0], self.doctrine["PATROL_ALT_RANGE"][1])

        # Find targets waypoints
        ingress, heading, distance = Conflict.frontline_vector(ally_cp, enemy_cp, self.game.theater)
        center = ingress.point_from_heading(heading, distance / 2)
        orbit_center = center.point_from_heading(heading - 90, random.randint(nm_to_meter(6), nm_to_meter(15)))

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

        # Note : Targets of a PATROL TRACK waypoints are the points to be defended
        orbit0.targets.append(flight.from_cp)
        orbit0.targets.append(center)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)


    def generate_sead(self, flight, location, custom_targets = []):
        """
        Generate a sead flight at a given location
        :param flight: Flight to setup
        :param location: Location of the SEAD target
        :param custom_targets: Custom targets if any
        """
        flight.points = []
        flight.flight_type = random.choice([FlightType.SEAD, FlightType.DEAD])

        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        heading = flight.from_cp.position.heading_between_point(location.position)
        ingress_heading = heading - 180 + 25
        egress_heading = heading - 180 - 25

        ingress_pos = location.position.point_from_heading(ingress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"])
        ingress_point = FlightWaypoint(
            FlightWaypointType.INGRESS_SEAD,
            ingress_pos.x,
            ingress_pos.y,
            self.doctrine["INGRESS_ALT"]
        )
        ingress_point.name = "INGRESS"
        ingress_point.pretty_name = "INGRESS on " + location.obj_name
        ingress_point.description = "INGRESS on " + location.obj_name
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
                    point.pretty_name = "DEAD on " + location.obj_name
                    point.only_for_player = True
                else:
                    point.description = "SEAD on " + location.obj_name
                    point.pretty_name = "SEAD on " + location.obj_name
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
                point.description = "DEAD on " + location.obj_name
                point.pretty_name = "DEAD on " + location.obj_name
                point.only_for_player = True
            else:
                point.description = "SEAD on " + location.obj_name
                point.pretty_name = "SEAD on " + location.obj_name
                point.only_for_player = True
            ingress_point.targets.append(location)
            ingress_point.targetGroup = location
            flight.points.append(point)

        egress_pos = location.position.point_from_heading(egress_heading, self.doctrine["INGRESS_EGRESS_DISTANCE"])
        egress_point = FlightWaypoint(
            FlightWaypointType.EGRESS,
            egress_pos.x,
            egress_pos.y,
            self.doctrine["EGRESS_ALT"]
        )
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS from " + location.obj_name
        egress_point.description = "EGRESS from " + location.obj_name
        flight.points.append(egress_point)

        descend = self.generate_descend_point(flight.from_cp)
        flight.points.append(descend)

        rtb = self.generate_rtb_waypoint(flight.from_cp)
        flight.points.append(rtb)


    def generate_cas(self, flight, from_cp, location):
        """
        Generate a CAS flight at a given location
        :param flight: Flight to setup
        :param location: Location of the CAS targets
        """
        is_helo = hasattr(flight.unit_type, "helicopter") and flight.unit_type.helicopter
        cap_alt = 1000
        flight.points = []
        flight.flight_type = FlightType.CAS

        ingress, heading, distance = Conflict.frontline_vector(from_cp, location, self.game.theater)
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

    def generate_ascend_point(self, from_cp):
        """
        Generate ascend point
        :param from_cp: Airport you're taking off from
        :return:
        """
        ascend_heading = from_cp.heading
        pos_ascend = from_cp.position.point_from_heading(ascend_heading, 10000)
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

    def generate_descend_point(self, from_cp):
        """
        Generate approach/descend point
        :param from_cp: Airport you're landing at
        :return:
        """
        ascend_heading = from_cp.heading
        descend = from_cp.position.point_from_heading(ascend_heading - 180, 10000)
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

    def generate_rtb_waypoint(self, from_cp):
        """
        Generate RTB landing point
        :param from_cp: Airport you're landing at
        :return:
        """
        rtb = from_cp.position
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
