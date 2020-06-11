import math
import operator
import random

from game import db
from gen import Conflict
from gen.flights.ai_flight_planner_db import INTERCEPT_CAPABLE, CAP_CAPABLE, CAS_CAPABLE, SEAD_CAPABLE, STRIKE_CAPABLE
from gen.flights.flight import Flight, FlightType, FlightWaypoint, FlightWaypointType


def meter_to_feet(value_in_meter):
    return int(3.28084 * value_in_meter)


def feet_to_meter(value_in_feet):
    return int(float(value_in_feet)/3.048)


def meter_to_nm(value_in_meter):
    return int(float(value_in_meter)*0.000539957)


def nm_to_meter(value_in_nm):
    return int(float(value_in_nm)*1852)


# TODO : Ideally should be based on the aircraft type instead / Availability of fuel
STRIKE_MAX_RANGE = 1500000
SEAD_MAX_RANGE = 1500000

MAX_NUMBER_OF_INTERCEPTION_GROUP = 3
MISSION_DURATION = 120 # in minutes
CAP_EVERY_X_MINUTES = 20
CAS_EVERY_X_MINUTES = 30
SEAD_EVERY_X_MINUTES = 40
STRIKE_EVERY_X_MINUTES = 40

INGRESS_EGRESS_DISTANCE = nm_to_meter(45)
INGRESS_ALT = feet_to_meter(20000)
EGRESS_ALT = feet_to_meter(20000)
PATROL_ALT_RANGE = (feet_to_meter(15000), feet_to_meter(33000))
NAV_ALT = 9144
PATTERN_ALTITUDE = feet_to_meter(5000)

CAP_DEFAULT_ENGAGE_DISTANCE = nm_to_meter(40)


class FlightPlanner:

    def __init__(self, from_cp, game):
        # TODO : have the flight planner depend on a 'stance' setting : [Defensive, Aggresive... etc] and faction doctrine
        # TODO : the flight planner should plan package and operations
        self.from_cp = from_cp
        self.game = game
        self.aircraft_inventory = {} # local copy of the airbase inventory

    def reset(self):
        """
        Reset the planned flights and available units
        """
        self.aircraft_inventory = dict({k: v for k, v in self.from_cp.base.aircraft.items()})
        self.interceptor_flights = []
        self.cap_flights = []
        self.cas_flights = []
        self.strike_flights = []
        self.sead_flights = []
        self.custom_flights = []
        self.flights = []
        self.potential_sead_targets = []
        self.potential_strike_targets = []

    def plan_flights(self):

        self.reset()
        self.compute_sead_targets()
        self.compute_strike_targets()

        # The priority is to assign air-superiority fighter or interceptor to interception roles, so they can scramble if there is an attacker
        #self.commision_interceptors()

        # Then some CAP patrol for the next 2 hours
        self.commision_cap()

        # Then setup cas
        self.commision_cas()

        # Then prepare some sead flights if required
        self.commision_sead()

        self.commision_strike()

        # TODO : commision ANTISHIP

    def remove_flight(self, index):
        try:
            flight = self.flights[index]
            if flight in self.interceptor_flights: self.interceptor_flights.remove(flight)
            if flight in self.cap_flights: self.cap_flights.remove(flight)
            if flight in self.cas_flights: self.cas_flights.remove(flight)
            if flight in self.strike_flights: self.strike_flights.remove(flight)
            if flight in self.sead_flights: self.sead_flights.remove(flight)
            if flight in self.custom_flights: self.custom_flights.remove(flight)
            self.flights.remove(flight)
        except IndexError:
            return


    def commision_interceptors(self):
        """
        Pick some aircraft to assign them to interception roles
        """

        # At least try to generate one interceptor group
        number_of_interceptor_groups = min(max(sum([v for k, v in self.aircraft_inventory.items()]) / 4, MAX_NUMBER_OF_INTERCEPTION_GROUP), 1)
        possible_interceptors = [k for k in self.aircraft_inventory.keys() if k in INTERCEPT_CAPABLE]

        if len(possible_interceptors) <= 0:
            possible_interceptors = [k for k,v in self.aircraft_inventory.items() if k in CAP_CAPABLE and v >= 2]

        if number_of_interceptor_groups > 0:
            inventory = dict({k: v for k, v in self.aircraft_inventory.items() if k in possible_interceptors})
            for i in range(number_of_interceptor_groups):
                try:
                    unit = random.choice([k for k,v in inventory.items() if v >= 2])
                except IndexError:
                    break
                inventory[unit] = inventory[unit] - 2
                flight = Flight(unit, 2, self.from_cp, FlightType.INTERCEPTION)
                flight.points = []

                self.interceptor_flights.append(flight)
                self.flights.append(flight)

            # Update inventory
            for k, v in inventory.items():
                self.aircraft_inventory[k] = v

    def commision_cap(self):
        """
        Pick some aircraft to assign them to defensive CAP roles (BARCAP)
        """

        possible_aircraft = [k for k, v in self.aircraft_inventory.items() if k in CAP_CAPABLE and v >= 2]
        inventory = dict({k: v for k, v in self.aircraft_inventory.items() if k in possible_aircraft})

        offset = random.randint(0,5)
        for i in range(int(MISSION_DURATION/CAP_EVERY_X_MINUTES)):

            try:
                unit = random.choice([k for k, v in inventory.items() if v >= 2])
            except IndexError:
                break

            inventory[unit] = inventory[unit] - 2
            flight = Flight(unit, 2, self.from_cp, FlightType.CAP)

            flight.points = []
            flight.scheduled_in = offset + i*random.randint(CAP_EVERY_X_MINUTES-5, CAP_EVERY_X_MINUTES+5)

            if len(self._get_cas_locations()) > 0:
                enemy_cp = random.choice(self._get_cas_locations())
                self.generate_frontline_cap(flight, flight.from_cp, enemy_cp)
            else:
                self.generate_barcap(flight, flight.from_cp)

            self.cap_flights.append(flight)
            self.flights.append(flight)

        # Update inventory
        for k, v in inventory.items():
            self.aircraft_inventory[k] = v

    def commision_cas(self):
        """
        Pick some aircraft to assign them to CAS
        """

        possible_aircraft = [k for k, v in self.aircraft_inventory.items() if k in CAS_CAPABLE and v >= 2]
        inventory = dict({k: v for k, v in self.aircraft_inventory.items() if k in possible_aircraft})
        cas_location = self._get_cas_locations()

        if len(cas_location) > 0:

            offset = random.randint(0,5)
            for i in range(int(MISSION_DURATION/CAS_EVERY_X_MINUTES)):

                try:
                    unit = random.choice([k for k, v in inventory.items() if v >= 2])
                except IndexError:
                    break

                inventory[unit] = inventory[unit] - 2
                flight = Flight(unit, 2, self.from_cp, FlightType.CAS)
                flight.points = []
                flight.scheduled_in = offset + i * random.randint(CAS_EVERY_X_MINUTES - 5, CAS_EVERY_X_MINUTES + 5)
                location = random.choice(cas_location)

                self.generate_cas(flight, flight.from_cp, location)

                self.cas_flights.append(flight)
                self.flights.append(flight)

            # Update inventory
            for k, v in inventory.items():
                self.aircraft_inventory[k] = v

    def commision_sead(self):
        """
        Pick some aircraft to assign them to SEAD tasks
        """

        possible_aircraft = [k for k, v in self.aircraft_inventory.items() if k in SEAD_CAPABLE and v >= 2]
        inventory = dict({k: v for k, v in self.aircraft_inventory.items() if k in possible_aircraft})

        if len(self.potential_sead_targets) > 0:

            offset = random.randint(0,5)
            for i in range(int(MISSION_DURATION/SEAD_EVERY_X_MINUTES)):

                if len(self.potential_sead_targets) <= 0:
                    break

                try:
                    unit = random.choice([k for k, v in inventory.items() if v >= 2])
                except IndexError:
                    break

                inventory[unit] = inventory[unit] - 2
                flight = Flight(unit, 2, self.from_cp, random.choice([FlightType.SEAD, FlightType.DEAD]))

                flight.points = []
                flight.scheduled_in = offset + i*random.randint(SEAD_EVERY_X_MINUTES-5, SEAD_EVERY_X_MINUTES+5)

                location = self.potential_sead_targets[0][0]
                self.potential_sead_targets.pop(0)

                self.generate_sead(flight, location, [])

                self.sead_flights.append(flight)
                self.flights.append(flight)

            # Update inventory
            for k, v in inventory.items():
                self.aircraft_inventory[k] = v


    def commision_strike(self):
        """
        Pick some aircraft to assign them to STRIKE tasks
        """
        possible_aircraft = [k for k, v in self.aircraft_inventory.items() if k in STRIKE_CAPABLE and v >= 2]
        inventory = dict({k: v for k, v in self.aircraft_inventory.items() if k in possible_aircraft})

        if len(self.potential_strike_targets) > 0:

            offset = random.randint(0,5)
            for i in range(int(MISSION_DURATION/STRIKE_EVERY_X_MINUTES)):

                if len(self.potential_strike_targets) <= 0:
                    break

                try:
                    unit = random.choice([k for k, v in inventory.items() if v >= 2])
                except IndexError:
                    break

                inventory[unit] = inventory[unit] - 2
                flight = Flight(unit, 2, self.from_cp, FlightType.STRIKE)

                flight.points = []
                flight.scheduled_in = offset + i*random.randint(SEAD_EVERY_X_MINUTES-5, SEAD_EVERY_X_MINUTES+5)

                location = self.potential_strike_targets[0][0]
                self.potential_strike_targets.pop(0)

                self.generate_strike(flight, location)

                self.strike_flights.append(flight)
                self.flights.append(flight)

            # Update inventory
            for k, v in inventory.items():
                self.aircraft_inventory[k] = v

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

            if distance > 2*STRIKE_MAX_RANGE:
                # Then it's unlikely any child ground object is in range
                return

            added_group = []
            for g in cp.ground_objects:
                if g.group_id in added_group or g.is_dead: continue

                # Compute distance to current cp
                distance = math.hypot(cp.position.x - self.from_cp.position.x,
                                      cp.position.y - self.from_cp.position.y)

                if distance < SEAD_MAX_RANGE:
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
            if distance > 2*SEAD_MAX_RANGE:
                return

            for g in cp.ground_objects:

                if g.dcs_identifier == "AA":

                    # Check that there is at least one unit with a radar in the ground objects unit groups
                    number_of_units = sum([len([r for r in group.units if hasattr(db.unit_type_from_name(r.type), "detection_range")
                                                and db.unit_type_from_name(r.type).detection_range > 1000]) for group in g.groups])
                    if number_of_units <= 0:
                        continue

                    # Compute distance to current cp
                    distance = math.hypot(cp.position.x - self.from_cp.position.x,
                                          cp.position.y - self.from_cp.position.y)

                    if distance < SEAD_MAX_RANGE:
                        self.potential_sead_targets.append((g, distance))

        self.potential_sead_targets.sort(key=operator.itemgetter(1))

    def __repr__(self):
        return "-"*40 + "\n" + self.from_cp.name + " planned flights :\n"\
               + "-"*40 + "\n" + "\n".join([repr(f) for f in self.flights]) + "\n" + "-"*40

    def get_available_aircraft(self):
        base_aircraft_inventory = dict({k: v for k, v in self.from_cp.base.aircraft.items()})
        for f in self.flights:
            if f.unit_type in base_aircraft_inventory.keys():
                base_aircraft_inventory[f.unit_type] = base_aircraft_inventory[f.unit_type] - f.count
                if base_aircraft_inventory[f.unit_type] <= 0:
                    del base_aircraft_inventory[f.unit_type]
        return base_aircraft_inventory


    def generate_strike(self, flight, location):

        flight.flight_type = FlightType.STRIKE
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        heading = flight.from_cp.position.heading_between_point(location.position)
        ingress_heading = heading - 180 + 25
        egress_heading = heading - 180 - 25

        ingress_pos = location.position.point_from_heading(ingress_heading, INGRESS_EGRESS_DISTANCE)
        ingress_point = FlightWaypoint(ingress_pos.x, ingress_pos.y, INGRESS_ALT)
        ingress_point.pretty_name = "INGRESS on " + location.obj_name
        ingress_point.description = "INGRESS on " + location.obj_name
        ingress_point.name = "INGRESS"
        ingress_point.waypoint_type = FlightWaypointType.INGRESS_STRIKE
        flight.points.append(ingress_point)

        if len(location.groups) > 0 and location.dcs_identifier == "AA":
            for g in location.groups:
                for j, u in enumerate(g.units):
                    point = FlightWaypoint(u.position.x, u.position.y, 0)
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

                    point = FlightWaypoint(building.position.x, building.position.y, 0)
                    point.description = "STRIKE on " + building.obj_name + " " + building.category + " [" + str(building.dcs_identifier) + " ]"
                    point.pretty_name = "STRIKE on " + building.obj_name + " " + building.category + " [" + str(building.dcs_identifier) + " ]"
                    point.name = building.obj_name
                    point.only_for_player = True
                    ingress_point.targets.append(building)
                    flight.points.append(point)
            else:
                point = FlightWaypoint(location.position.x, location.position.y, 0)
                point.description = "STRIKE on " + location.obj_name
                point.pretty_name = "STRIKE on " + location.obj_name
                point.name = location.obj_name
                point.only_for_player = True
                ingress_point.targets.append(location)
                flight.points.append(point)

        egress_pos = location.position.point_from_heading(egress_heading, INGRESS_EGRESS_DISTANCE)
        egress_point = FlightWaypoint(egress_pos.x, egress_pos.y, EGRESS_ALT)
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS from " + location.obj_name
        egress_point.description = "EGRESS from " + location.obj_name
        egress_point.waypoint_type = FlightWaypointType.EGRESS
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
        :param location: Location to protect in priority
        :param location: Is the location to protect a frontline
        """
        flight.flight_type = FlightType.BARCAP if for_cp.is_carrier else FlightType.CAP
        patrol_alt = random.randint(PATROL_ALT_RANGE[0], PATROL_ALT_RANGE[1])

        if len(for_cp.ground_objects) > 0:
            loc = random.choice(for_cp.ground_objects)
            hdg = for_cp.position.heading_between_point(loc.position)
            radius = nm_to_meter(random.randint(15, 40))
            orbit0p = loc.position.point_from_heading(hdg - 90, radius)
            orbit1p = loc.position.point_from_heading(hdg + 90, radius)
        else:
            loc = for_cp.position.point_from_heading(random.randint(0, 360), random.randint(nm_to_meter(10), nm_to_meter(40)))
            hdg = for_cp.position.heading_between_point(loc)
            radius = nm_to_meter(random.randint(15, 40))
            orbit0p = loc.point_from_heading(hdg - 90, radius)
            orbit1p = loc.point_from_heading(hdg + 90, radius)

        # Create points
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        orbit0 = FlightWaypoint(orbit0p.x, orbit0p.y, patrol_alt)
        orbit0.name = "ORBIT 0"
        orbit0.description = "Standby between this point and the next one"
        orbit0.pretty_name = "Race-track start"
        orbit0.waypoint_type = FlightWaypointType.PATROL_TRACK
        flight.points.append(orbit0)

        orbit1 = FlightWaypoint(orbit1p.x, orbit1p.y, patrol_alt)
        orbit1.name = "ORBIT 1"
        orbit1.description = "Standby between this point and the previous one"
        orbit1.pretty_name = "Race-track end"
        orbit1.waypoint_type = FlightWaypointType.PATROL
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
        patrol_alt = random.randint(PATROL_ALT_RANGE[0], PATROL_ALT_RANGE[1])

        # Find targets waypoints
        ingress, heading, distance = Conflict.frontline_vector(ally_cp, enemy_cp, self.game.theater)
        center = ingress.point_from_heading(heading, distance / 2)
        orbit_center = center.point_from_heading(heading - 90, random.randint(nm_to_meter(6), nm_to_meter(15)))
        radius = distance * 2
        orbit0p = orbit_center.point_from_heading(heading, radius)
        orbit1p = orbit_center.point_from_heading(heading + 180, radius)

        # Create points
        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        orbit0 = FlightWaypoint(orbit0p.x, orbit0p.y, patrol_alt)
        orbit0.name = "ORBIT 0"
        orbit0.description = "Standby between this point and the next one"
        orbit0.pretty_name = "Race-track start"
        orbit0.waypoint_type = FlightWaypointType.PATROL_TRACK
        flight.points.append(orbit0)

        orbit1 = FlightWaypoint(orbit1p.x, orbit1p.y, patrol_alt)
        orbit1.name = "ORBIT 1"
        orbit1.description = "Standby between this point and the previous one"
        orbit1.pretty_name = "Race-track end"
        orbit1.waypoint_type = FlightWaypointType.PATROL
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

        ingress_pos = location.position.point_from_heading(ingress_heading, INGRESS_EGRESS_DISTANCE)
        ingress_point = FlightWaypoint(ingress_pos.x, ingress_pos.y, INGRESS_ALT)
        ingress_point.name = "INGRESS"
        ingress_point.pretty_name = "INGRESS on " + location.obj_name
        ingress_point.description = "INGRESS on " + location.obj_name
        ingress_point.waypoint_type = FlightWaypointType.INGRESS_SEAD
        flight.points.append(ingress_point)

        if len(custom_targets) > 0:
            for target in custom_targets:
                point = FlightWaypoint(target.position.x, target.position.y, 0)
                point.alt_type = "RADIO"
                if flight.flight_type == FlightType.DEAD:
                    point.description = "SEAD on " + target.type
                    point.pretty_name = "SEAD on " + location.obj_name
                    point.only_for_player = True
                else:
                    point.description = "DEAD on " + location.obj_name
                    point.pretty_name = "DEAD on " + location.obj_name
                    point.only_for_player = True
                ingress_point.targets.append(location)
                flight.points.append(point)
        else:
            point = FlightWaypoint(location.position.x, location.position.y, 0)
            point.alt_type = "RADIO"
            if flight.flight_type == FlightType.DEAD:
                point.description = "SEAD on " + location.obj_name
                point.pretty_name = "SEAD on " + location.obj_name
                point.only_for_player = True
            else:
                point.description = "DEAD on " + location.obj_name
                point.pretty_name = "DEAD on " + location.obj_name
                point.only_for_player = True
            ingress_point.targets.append(location)
            flight.points.append(point)

        egress_pos = location.position.point_from_heading(egress_heading, INGRESS_EGRESS_DISTANCE)
        egress_point = FlightWaypoint(egress_pos.x, egress_pos.y, EGRESS_ALT)
        egress_point.name = "INGRESS"
        egress_point.pretty_name = "EGRESS from " + location.obj_name
        egress_point.description = "EGRESS from " + location.obj_name
        egress_point.waypoint_type = FlightWaypointType.EGRESS
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

        flight.points = []
        flight.flight_type = FlightType.CAS

        ingress, heading, distance = Conflict.frontline_vector(from_cp, location, self.game.theater)
        center = ingress.point_from_heading(heading, distance / 2)
        egress = ingress.point_from_heading(heading, distance)

        ascend = self.generate_ascend_point(flight.from_cp)
        flight.points.append(ascend)

        ingress_point = FlightWaypoint(ingress.x, ingress.y, 1000)
        ingress_point.alt_type = "RADIO"
        ingress_point.name = "INGRESS"
        ingress_point.pretty_name = "INGRESS"
        ingress_point.description = "Ingress into CAS area"
        ingress_point.waypoint_type = FlightWaypointType.INGRESS_CAS
        flight.points.append(ingress_point)

        center_point = FlightWaypoint(center.x, center.y, 1000)
        center_point.alt_type = "RADIO"
        center_point.description = "Provide CAS"
        center_point.name = "CAS"
        center_point.pretty_name = "CAS"
        center_point.waypoint_type = FlightWaypointType.CAS
        flight.points.append(center_point)

        egress_point = FlightWaypoint(egress.x, egress.y, 1000)
        egress_point.alt_type = "RADIO"
        egress_point.description = "Egress from CAS area"
        egress_point.name = "EGRESS"
        egress_point.pretty_name = "EGRESS"
        egress_point.waypoint_type = FlightWaypointType.EGRESS
        flight.points.append(egress_point)

        descend = self.generate_descend_point(flight.from_cp)
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
        ascend = FlightWaypoint(pos_ascend.x, pos_ascend.y, PATTERN_ALTITUDE)
        ascend.name = "ASCEND"
        ascend.alt_type = "RADIO"
        ascend.description = "Ascend to alt [" + str(meter_to_feet(PATTERN_ALTITUDE)) + " ft AGL], then proceed to next waypoint"
        ascend.pretty_name = "Ascend to alt [" + str(meter_to_feet(PATTERN_ALTITUDE)) + " ft AGL]"
        ascend.waypoint_type = FlightWaypointType.ASCEND_POINT
        return ascend


    def generate_descend_point(self, from_cp):
        """
        Generate approach/descend point
        :param from_cp: Airport you're landing at
        :return:
        """
        ascend_heading = from_cp.heading
        descend = from_cp.position.point_from_heading(ascend_heading - 180, 10000)
        descend = FlightWaypoint(descend.x, descend.y, PATTERN_ALTITUDE)
        descend.name = "DESCEND"
        descend.alt_type = "RADIO"
        descend.description = "Descend to pattern alt [" + str(meter_to_feet(PATTERN_ALTITUDE)) + " ft AGL], contact tower, and land"
        descend.pretty_name = "Descend to pattern alt [" + str(meter_to_feet(PATTERN_ALTITUDE)) + " ft AGL]"
        descend.waypoint_type = FlightWaypointType.DESCENT_POINT
        return descend


    def generate_rtb_waypoint(self, from_cp):
        """
        Generate RTB landing point
        :param from_cp: Airport you're landing at
        :return:
        """
        rtb = from_cp.position
        rtb = FlightWaypoint(rtb.x, rtb.y, 0)
        rtb.name = "LANDING"
        rtb.alt_type = "RADIO"
        rtb.description = "RTB"
        rtb.pretty_name = "RTB"
        rtb.waypoint_type = FlightWaypointType.LANDING_POINT
        return rtb