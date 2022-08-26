from __future__ import annotations

from datetime import timedelta
from typing import Type

from dcs import Point

from game.utils import Distance, Heading, feet, meters
from .ibuilder import IBuilder
from .patrolling import PatrollingLayout
from .refuelingflightplan import RefuelingFlightPlan
from .waypointbuilder import WaypointBuilder
from ..flightwaypoint import FlightWaypoint
from ..flightwaypointtype import FlightWaypointType


class PackageRefuelingFlightPlan(RefuelingFlightPlan):
    @staticmethod
    def builder_type() -> Type[Builder]:
        return Builder

    @property
    def patrol_duration(self) -> timedelta:
        # TODO: Only consider aircraft that can refuel with this tanker type.
        refuel_time_minutes = 5
        for self.flight in self.package.flights:
            flight_size = self.flight.roster.max_size
            refuel_time_minutes = refuel_time_minutes + 4 * flight_size + 1

        return timedelta(minutes=refuel_time_minutes)

    def target_area_waypoint(self) -> FlightWaypoint:
        return FlightWaypoint(
            "TARGET AREA",
            FlightWaypointType.TARGET_GROUP_LOC,
            self.package.target.position,
            meters(0),
            "RADIO",
        )

    @property
    def patrol_start_time(self) -> timedelta:
        altitude = self.flight.unit_type.patrol_altitude

        if altitude is None:
            altitude = Distance.from_feet(20000)

        assert self.package.waypoints is not None

        # Cheat in a FlightWaypoint for the split point.
        split: Point = self.package.waypoints.split
        split_waypoint: FlightWaypoint = FlightWaypoint(
            "SPLIT", FlightWaypointType.SPLIT, split, altitude
        )

        # Cheat in a FlightWaypoint for the refuel point.
        refuel: Point = self.package.waypoints.refuel
        refuel_waypoint: FlightWaypoint = FlightWaypoint(
            "REFUEL", FlightWaypointType.REFUEL, refuel, altitude
        )

        delay_target_to_split: timedelta = self.travel_time_between_waypoints(
            self.target_area_waypoint(), split_waypoint
        )
        delay_split_to_refuel: timedelta = self.travel_time_between_waypoints(
            split_waypoint, refuel_waypoint
        )

        return (
            self.package.time_over_target
            + delay_target_to_split
            + delay_split_to_refuel
            - timedelta(minutes=1.5)
        )


class Builder(IBuilder[PackageRefuelingFlightPlan, PatrollingLayout]):
    def layout(self) -> PatrollingLayout:
        package_waypoints = self.package.waypoints
        assert package_waypoints is not None

        racetrack_half_distance = Distance.from_nautical_miles(20).meters

        racetrack_center = package_waypoints.refuel

        split_heading = Heading.from_degrees(
            racetrack_center.heading_between_point(package_waypoints.split)
        )
        home_heading = split_heading.opposite

        racetrack_start = racetrack_center.point_from_heading(
            split_heading.degrees, racetrack_half_distance
        )

        racetrack_end = racetrack_center.point_from_heading(
            home_heading.degrees, racetrack_half_distance
        )

        builder = WaypointBuilder(self.flight, self.coalition)

        tanker_type = self.flight.unit_type
        if tanker_type.patrol_altitude is not None:
            altitude = tanker_type.patrol_altitude
        else:
            altitude = feet(21000)

        racetrack = builder.race_track(racetrack_start, racetrack_end, altitude)

        return PatrollingLayout(
            departure=builder.takeoff(self.flight.departure),
            nav_to=builder.nav_path(
                self.flight.departure.position, racetrack_start, altitude
            ),
            nav_from=builder.nav_path(
                racetrack_end, self.flight.arrival.position, altitude
            ),
            patrol_start=racetrack[0],
            patrol_end=racetrack[1],
            arrival=builder.land(self.flight.arrival),
            divert=builder.divert(self.flight.divert),
            bullseye=builder.bullseye(),
        )

    def build(self) -> PackageRefuelingFlightPlan:
        return PackageRefuelingFlightPlan(self.flight, self.layout())
