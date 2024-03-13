from __future__ import annotations

import heapq
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Union

from dcs.mapping import Point
from shapely.geometry import (
    LineString,
    MultiPolygon,
    Point as ShapelyPoint,
    Polygon,
    box,
)
from shapely.ops import nearest_points, triangulate

from game.theater import ConflictTheater
from game.threatzones import ThreatZones
from game.utils import nautical_miles


class NavMeshError(RuntimeError):
    pass


class NavMeshPoly:
    def __init__(self, ident: int, poly: Polygon, threatened: bool) -> None:
        self.ident = ident
        self.poly = poly
        self.threatened = threatened
        self.neighbors: Dict[NavMeshPoly, Union[LineString, ShapelyPoint]] = {}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NavMeshPoly):
            return False
        return self.ident == other.ident

    def __hash__(self) -> int:
        return self.ident


@dataclass(frozen=True)
class NavPoint:
    point: ShapelyPoint
    poly: NavMeshPoly

    def world_point(self, theater: ConflictTheater) -> Point:
        return Point(self.point.x, self.point.y, theater.terrain)

    def __hash__(self) -> int:
        return hash(self.poly.ident)

    def __eq__(self, other: object) -> bool:
        if id(self) == id(other):
            return True

        if not isinstance(other, NavPoint):
            return False

        # The tolerance value used here is the same that was used by the now deprecated
        # almost_equals.
        if not self.point.equals_exact(other.point, 0.5 * 10 ** (-6)):
            return False

        return self.poly == other.poly

    def __str__(self) -> str:
        return f"{self.point} in {self.poly.ident}"


@dataclass(frozen=True, order=True)
class FrontierNode:
    cost: float
    point: NavPoint = field(compare=False)


class NavFrontier:
    def __init__(self) -> None:
        self.nodes: List[FrontierNode] = []

    def push(self, poly: NavPoint, cost: float) -> None:
        heapq.heappush(self.nodes, FrontierNode(cost, poly))

    def pop(self) -> Optional[NavPoint]:
        try:
            return heapq.heappop(self.nodes).point
        except IndexError:
            return None


class NavMesh:
    def __init__(self, polys: List[NavMeshPoly], theater: ConflictTheater) -> None:
        self.polys = polys
        self.theater = theater

    def localize(self, point: Point) -> Optional[NavMeshPoly]:
        # This is a naive implementation but it's O(n). Runs at about 10k
        # lookups a second on a 5950X. Flights usually have 5-10 waypoints, so
        # that's 1k-2k flights before we lose a full second to localization as a
        # part of flight plan creation.
        #
        # Can improve the algorithm later if needed, but that seems unnecessary
        # currently.
        p = ShapelyPoint(point.x, point.y)
        for navpoly in self.polys:
            if navpoly.poly.intersects(p):
                return navpoly
        return None

    @staticmethod
    def travel_cost(a: NavPoint, b: NavPoint) -> float:
        modifier = 1.0
        if a.poly.threatened:
            modifier = 3.0
        return a.point.distance(b.point) * modifier

    def travel_heuristic(self, a: NavPoint, b: NavPoint) -> float:
        return self.travel_cost(a, b)

    def reconstruct_path(
        self,
        came_from: Dict[NavPoint, Optional[NavPoint]],
        origin: NavPoint,
        destination: NavPoint,
    ) -> List[Point]:
        current = destination
        path: List[Point] = []
        while current != origin:
            path.append(current.world_point(self.theater))
            previous = came_from[current]
            if previous is None:
                raise NavMeshError(
                    f"Could not reconstruct path to {destination} from {origin}"
                )
            current = previous
        path.append(origin.world_point(self.theater))
        path.reverse()
        return path

    @staticmethod
    def dcs_to_shapely_point(point: Point) -> ShapelyPoint:
        return ShapelyPoint(point.x, point.y)

    def shortest_path(self, origin: Point, destination: Point) -> List[Point]:
        origin_poly = self.localize(origin)
        if origin_poly is None:
            raise NavMeshError(f"Origin point {origin} is outside the navmesh")
        destination_poly = self.localize(destination)
        if destination_poly is None:
            raise NavMeshError(
                f"Destination point {destination} is outside the navmesh"
            )

        return self._shortest_path(
            NavPoint(self.dcs_to_shapely_point(origin), origin_poly),
            NavPoint(self.dcs_to_shapely_point(destination), destination_poly),
        )

    def _shortest_path(self, origin: NavPoint, destination: NavPoint) -> List[Point]:
        # Adapted from
        # https://www.redblobgames.com/pathfinding/a-star/implementation.py.
        frontier = NavFrontier()
        frontier.push(origin, 0.0)
        came_from: Dict[NavPoint, Optional[NavPoint]] = {origin: None}

        best_known: Dict[NavPoint, float] = defaultdict(lambda: math.inf)
        best_known[origin] = 0.0

        while (current := frontier.pop()) is not None:
            if current == destination:
                break

            if current.poly == destination.poly:
                # Made it to the correct nav poly. Add the leg from the border
                # to the target.
                cost = best_known[current] + self.travel_cost(current, destination)
                if cost < best_known[destination]:
                    best_known[destination] = cost
                    estimated = cost
                    frontier.push(destination, estimated)
                    came_from[destination] = current

            for neighbor, boundary in current.poly.neighbors.items():
                previous = came_from[current]
                if previous is not None and previous.poly == neighbor:
                    # Don't backtrack.
                    continue
                if previous is None and current != origin:
                    raise RuntimeError
                _, neighbor_point = nearest_points(current.point, boundary)
                neighbor_nav = NavPoint(neighbor_point, neighbor)
                cost = best_known[current] + self.travel_cost(current, neighbor_nav)
                if cost < best_known[neighbor_nav]:
                    best_known[neighbor_nav] = cost
                    estimated = cost + self.travel_heuristic(neighbor_nav, destination)
                    frontier.push(neighbor_nav, estimated)
                    came_from[neighbor_nav] = current

        return self.reconstruct_path(came_from, origin, destination)

    @staticmethod
    def map_bounds(theater: ConflictTheater) -> Polygon:
        points = []
        for cp in theater.controlpoints:
            points.append(ShapelyPoint(cp.position.x, cp.position.y))
            for tgo in cp.ground_objects:
                points.append(ShapelyPoint(tgo.position.x, tgo.position.y))
        # Needs to be a large enough boundary beyond the known points so that
        # threatened airbases at the map edges have room to retreat from the
        # threat without running off the navmesh.
        return box(*LineString(points).bounds).buffer(
            nautical_miles(200).meters, resolution=1
        )

    @staticmethod
    def create_navpolys(
        polys: List[Polygon], threat_zones: ThreatZones
    ) -> List[NavMeshPoly]:
        return [
            NavMeshPoly(i, p, threat_zones.threatened(p)) for i, p in enumerate(polys)
        ]

    @staticmethod
    def associate_neighbors(polys: List[NavMeshPoly]) -> None:
        # Maps (rounded) points to polygons that have a vertex at that point.
        # The points are rounded to the nearest int so we can use them as dict
        # keys. This allows us to perform approximate neighbor lookups more
        # efficiently than comparing each poly to every other poly by finding
        # approximate neighbors before checking if the polys actually touch.
        points_map: Dict[Tuple[int, int], Set[NavMeshPoly]] = defaultdict(set)

        for navpoly in polys:
            # The coordinates of the polygon's boundary are a sequence of
            # coordinates that define the polygon. The first point is repeated
            # at the end, so skip the last vertex.
            for x, y in navpoly.poly.boundary.coords[:-1]:
                point = (int(x), int(y))
                neighbors = {}
                for potential_neighbor in points_map[point]:
                    intersection = navpoly.poly.intersection(potential_neighbor.poly)
                    if not intersection.is_empty:
                        potential_neighbor.neighbors[navpoly] = intersection
                        neighbors[potential_neighbor] = intersection
                navpoly.neighbors.update(neighbors)
                points_map[point].add(navpoly)

    @classmethod
    def from_threat_zones(
        cls, threat_zones: ThreatZones, theater: ConflictTheater
    ) -> NavMesh:
        # Simplify the threat poly to reduce the number of nav zones. Increase
        # the size of the zone and then simplify it with the buffer size as the
        # error margin. This will create a simpler poly around the threat zone.
        buffer = nautical_miles(10).meters
        threat_poly = threat_zones.all.buffer(buffer).simplify(buffer)

        # Threat zones can be disconnected. Create a list of threat zones.
        if isinstance(threat_poly, MultiPolygon):
            polys = list(threat_poly.geoms)
        else:
            polys = [threat_poly]

        # Subtract the threat zones from the whole-map poly to build a navmesh
        # for the *safe* areas. Navigation within threatened regions is always
        # a straight line to the target or out of the threatened region.
        bounds = cls.map_bounds(theater)
        for poly in polys:
            bounds = bounds.difference(poly)

        # Triangulate the safe-region to build the navmesh.
        navpolys = cls.create_navpolys(triangulate(bounds), threat_zones)
        cls.associate_neighbors(navpolys)
        return NavMesh(navpolys, theater)
