from __future__ import annotations

import heapq
import math
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Iterator, List, Optional, Set, Tuple

from .conflicttheater import ConflictTheater
from .controlpoint import ControlPoint


class NoPathError(RuntimeError):
    def __init__(self, origin: ControlPoint, destination: ControlPoint) -> None:
        super().__init__(f"Could not reconstruct path to {destination} from {origin}")


@dataclass(frozen=True, order=True)
class FrontierNode:
    cost: float
    point: ControlPoint = field(compare=False)


class Frontier:
    def __init__(self) -> None:
        self.nodes: List[FrontierNode] = []

    def push(self, poly: ControlPoint, cost: float) -> None:
        heapq.heappush(self.nodes, FrontierNode(cost, poly))

    def pop(self) -> Optional[FrontierNode]:
        try:
            return heapq.heappop(self.nodes)
        except IndexError:
            return None

    def __bool__(self) -> bool:
        return bool(self.nodes)


class TransitConnection(Enum):
    Road = auto()
    Shipping = auto()
    Airlift = auto()


class TransitNetwork:
    def __init__(self) -> None:
        self.nodes: Dict[
            ControlPoint, Dict[ControlPoint, TransitConnection]
        ] = defaultdict(dict)

    def has_destinations(self, control_point: ControlPoint) -> bool:
        return bool(self.nodes[control_point])

    def has_link(self, a: ControlPoint, b: ControlPoint) -> bool:
        return b in self.nodes[a]

    def link_type(self, a: ControlPoint, b: ControlPoint) -> TransitConnection:
        return self.nodes[a][b]

    def link_with(
        self, a: ControlPoint, b: ControlPoint, link_type: TransitConnection
    ) -> None:
        self.nodes[a][b] = link_type
        self.nodes[b][a] = link_type

    def link_road(self, a: ControlPoint, b: ControlPoint) -> None:
        self.link_with(a, b, TransitConnection.Road)

    def link_shipping(self, a: ControlPoint, b: ControlPoint) -> None:
        self.link_with(a, b, TransitConnection.Shipping)

    def link_airport(self, a: ControlPoint, b: ControlPoint) -> None:
        self.link_with(a, b, TransitConnection.Airlift)

    def connections_from(self, control_point: ControlPoint) -> Iterator[ControlPoint]:
        yield from self.nodes[control_point]

    def cost(self, a: ControlPoint, b: ControlPoint) -> float:
        return {
            TransitConnection.Road: 1,
            TransitConnection.Shipping: 3,
            # Set arbitrarily high so that other methods are preferred, but still scaled
            # by distance so that when we do need it we still pick the closest airfield.
            # The units of distance are meters so there's no risk of these
            TransitConnection.Airlift: a.position.distance_to_point(b.position),
        }[self.link_type(a, b)]

    def has_path_between(
        self,
        origin: ControlPoint,
        destination: ControlPoint,
        seen: Optional[set[ControlPoint]] = None,
    ) -> bool:
        if seen is None:
            seen = set()
        seen.add(origin)
        for connection in self.connections_from(origin):
            if connection in seen:
                continue
            if connection == destination:
                return True
            if self.has_path_between(connection, destination, seen):
                return True
        return False

    def shortest_path_between(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> list[ControlPoint]:
        return self.shortest_path_with_cost(origin, destination)[0]

    def shortest_path_with_cost(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> Tuple[List[ControlPoint], float]:
        if origin not in self.nodes:
            raise ValueError(f"{origin} is not in the transit network.")
        if destination not in self.nodes:
            raise ValueError(f"{destination} is not in the transit network.")

        frontier = Frontier()
        frontier.push(origin, 0)

        came_from: Dict[ControlPoint, Optional[ControlPoint]] = {origin: None}

        best_known: Dict[ControlPoint, float] = defaultdict(lambda: math.inf)
        best_known[origin] = 0.0

        while (node := frontier.pop()) is not None:
            cost = node.cost
            current = node.point
            if cost > best_known[current]:
                continue

            for neighbor in self.connections_from(current):
                new_cost = cost + self.cost(node.point, neighbor)
                if new_cost < best_known[neighbor]:
                    best_known[neighbor] = new_cost
                    frontier.push(neighbor, new_cost)
                    came_from[neighbor] = current

        # Reconstruct and reverse the path.
        current = destination
        path: List[ControlPoint] = []
        while current != origin:
            path.append(current)
            previous = came_from.get(current)
            if previous is None:
                raise NoPathError(origin, destination)
            current = previous
        path.reverse()
        return path, best_known[destination]


class TransitNetworkBuilder:
    def __init__(self, theater: ConflictTheater, for_player: bool) -> None:
        self.control_points = list(theater.control_points_for(for_player))
        self.network = TransitNetwork()
        self.airports: Set[ControlPoint] = {
            cp
            for cp in self.control_points
            if cp.is_friendly(for_player) and cp.runway_is_operational()
        }

    def build(self) -> TransitNetwork:
        seen = set()
        for control_point in self.control_points:
            if control_point not in seen:
                seen.add(control_point)
                self.add_transit_links(control_point)
        return self.network

    def add_transit_links(self, control_point: ControlPoint) -> None:
        # Prefer road connections.
        for road_connection in control_point.connected_points:
            if road_connection.is_friendly_to(control_point):
                self.network.link_road(control_point, road_connection)

        # Use sea connections if there's no road or rail connection.
        for sea_connection in control_point.shipping_lanes:
            if self.network.has_link(control_point, sea_connection):
                continue
            if sea_connection.is_friendly_to(control_point):
                self.network.link_shipping(control_point, sea_connection)

        # And use airports as a last resort.
        if control_point in self.airports:
            for airport in self.airports:
                if control_point == airport:
                    continue
                if self.network.has_link(control_point, airport):
                    continue
                if not airport.is_friendly_to(control_point):
                    continue
                self.network.link_airport(control_point, airport)
