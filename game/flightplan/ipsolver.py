from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from shapely.geometry import MultiPolygon, Point
from shapely.geometry.base import BaseGeometry

from game.data.doctrine import Doctrine
from game.flightplan.waypointsolver import WaypointSolver
from game.flightplan.waypointstrategy import WaypointStrategy
from game.utils import meters, nautical_miles

MIN_DISTANCE_FROM_DEPARTURE = nautical_miles(5)


class ThreatTolerantIpStrategy(WaypointStrategy):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__(threat_zones)
        self.prerequisite(target).min_distance_from(
            departure, doctrine.min_ingress_distance
        )
        self.require().at_least(MIN_DISTANCE_FROM_DEPARTURE).away_from(departure)
        self.require().at_most(meters(departure.distance(target))).away_from(departure)
        self.require().at_least(doctrine.min_ingress_distance).away_from(target)
        max_ip_range = min(
            doctrine.max_ingress_distance, meters(departure.distance(target))
        )
        self.require().at_most(max_ip_range).away_from(target)
        self.threat_tolerance(target, max_ip_range, nautical_miles(5))
        self.nearest(departure)


class UnsafeIpStrategy(WaypointStrategy):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__(threat_zones)
        self.prerequisite(target).min_distance_from(
            departure, doctrine.min_ingress_distance
        )
        self.require().at_least(MIN_DISTANCE_FROM_DEPARTURE).away_from(
            departure, "departure"
        )
        self.require().at_most(meters(departure.distance(target))).away_from(
            departure, "departure"
        )
        self.require().at_least(doctrine.min_ingress_distance).away_from(
            target, "target"
        )
        max_ip_range = min(
            doctrine.max_ingress_distance, meters(departure.distance(target))
        )
        self.require().at_most(max_ip_range).away_from(target, "target")
        self.nearest(departure)


class SafeIpStrategy(WaypointStrategy):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__(threat_zones)
        self.prerequisite(departure).is_safe()
        self.prerequisite(target).min_distance_from(
            departure, doctrine.min_ingress_distance
        )
        self.require().at_least(MIN_DISTANCE_FROM_DEPARTURE).away_from(
            departure, "departure"
        )
        self.require().at_most(meters(departure.distance(target))).away_from(
            departure, "departure"
        )
        self.require().at_least(doctrine.min_ingress_distance).away_from(
            target, "target"
        )
        self.require().at_most(
            min(doctrine.max_ingress_distance, meters(departure.distance(target)))
        ).away_from(target, "target")
        self.require().safe()
        self.nearest(departure)


class SafeBackTrackingIpStrategy(WaypointStrategy):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__(threat_zones)
        self.require().at_least(MIN_DISTANCE_FROM_DEPARTURE).away_from(
            departure, "departure"
        )
        self.require().at_least(doctrine.min_ingress_distance).away_from(
            target, "target"
        )
        self.require().at_most(doctrine.max_ingress_distance).away_from(
            target, "target"
        )
        self.require().safe()
        self.nearest(departure)


class UnsafeBackTrackingIpStrategy(WaypointStrategy):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__(threat_zones)
        self.require().at_least(MIN_DISTANCE_FROM_DEPARTURE).away_from(
            departure, "departure"
        )
        self.require().at_least(doctrine.min_ingress_distance).away_from(
            target, "target"
        )
        self.require().at_most(doctrine.max_ingress_distance).away_from(
            target, "target"
        )
        self.nearest(departure)


class IpSolver(WaypointSolver):
    def __init__(
        self,
        departure: Point,
        target: Point,
        doctrine: Doctrine,
        threat_zones: MultiPolygon,
    ) -> None:
        super().__init__()
        self.departure = departure
        self.target = target
        self.doctrine = doctrine
        self.threat_zones = threat_zones

        self.add_strategy(SafeIpStrategy(departure, target, doctrine, threat_zones))
        self.add_strategy(
            ThreatTolerantIpStrategy(departure, target, doctrine, threat_zones)
        )
        self.add_strategy(UnsafeIpStrategy(departure, target, doctrine, threat_zones))
        self.add_strategy(
            SafeBackTrackingIpStrategy(departure, target, doctrine, threat_zones)
        )
        # TODO: The cases that require this are not covered by any tests.
        self.add_strategy(
            UnsafeBackTrackingIpStrategy(departure, target, doctrine, threat_zones)
        )

    def describe_metadata(self) -> dict[str, Any]:
        return {"doctrine": self.doctrine.name}

    def describe_inputs(self) -> Iterator[tuple[str, BaseGeometry]]:
        yield "departure", self.departure
        yield "target", self.target
        yield "threat_zones", self.threat_zones
