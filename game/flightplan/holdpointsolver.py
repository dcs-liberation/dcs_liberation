from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from shapely.geometry import MultiPolygon, Point
from shapely.geometry.base import BaseGeometry

from game.ato import Flight
from game.data.doctrine import Doctrine
from game.flightplan.waypointsolver import WaypointSolver
from game.flightplan.waypointstrategy import WaypointStrategy
from game.persistence.paths import waypoint_debug_directory
from game.utils import nautical_miles, meters, Heading, dcs_to_shapely_point

MIN_DISTANCE_FROM_DEPARTURE = nautical_miles(5)


class HoldPointStrategy(WaypointStrategy):
    def __init__(
        self,
        departure: Point,
        target: Point,
        ip: Point,
        join: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__(threat_zones)
        join_to_target_distance = meters(join.distance(target))
        self.require().safe()
        self.require().at_least(doctrine.push_distance).away_from(join)
        self.require().at_least(join_to_target_distance).away_from(target)
        self.require().at_least(doctrine.hold_distance).away_from(departure)
        self.require().maximum_turn_to(join, ip, Heading.from_degrees(40))
        self.nearest(departure)


class HoldPointSolver(WaypointSolver):
    def __init__(
        self,
        departure: Point,
        target: Point,
        ip: Point,
        join: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__()
        self.departure = departure
        self.target = target
        self.ip = ip
        self.join = join
        self.doctrine = doctrine
        self.threat_zones = threat_zones

        self.add_strategy(
            HoldPointStrategy(departure, target, ip, join, doctrine, threat_zones)
        )

    def describe_metadata(self) -> dict[str, Any]:
        return {"doctrine": self.doctrine.name}

    def describe_inputs(self) -> Iterator[tuple[str, BaseGeometry]]:
        yield "departure", self.departure
        yield "target", self.target
        yield "ip", self.ip
        yield "join", self.join
        yield "threat_zones", self.threat_zones

    @staticmethod
    def solve_for_flight(flight: Flight, dump_debug_info: bool) -> Point:
        assert flight.package.waypoints is not None
        # Start by picking the best IP for the attack.
        solver = HoldPointSolver(
            dcs_to_shapely_point(flight.departure.position),
            dcs_to_shapely_point(flight.package.target.position),
            dcs_to_shapely_point(flight.package.waypoints.ingress),
            dcs_to_shapely_point(flight.package.waypoints.join),
            flight.coalition.doctrine,
            flight.coalition.opponent.threat_zone.all,
        )
        solver.set_debug_properties(
            waypoint_debug_directory() / "Hold", flight.coalition.game.theater.terrain
        )
        hold_point = solver.solve()
        if dump_debug_info:
            solver.dump_debug_info()

        return flight.departure.position.new_in_same_map(hold_point.x, hold_point.y)
