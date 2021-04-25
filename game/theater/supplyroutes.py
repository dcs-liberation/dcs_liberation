from __future__ import annotations

import heapq
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, Iterator, List, Optional

from game.theater.controlpoint import ControlPoint


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


# TODO: Build a single SupplyRoute for each coalition at the start of the turn.
# Supply routes need to cover the whole network to support multi-mode links.
#
# Traverse each friendly control point and build out a network from each. Nodes create
# connections to:
#
# 1. Bases connected by road
# 2. Bases connected by rail
# 3. Bases connected by shipping lane
# 4. Airports large enough to operate cargo planes connect to each other
# 5. Airports capable of operating helicopters connect to other airports within cargo
#    helicopter range, and FOBs within half of the range (since they can't be refueled
#    at the drop off).
#
# The costs of each link would be set such that the above order roughly corresponds to
# the prevalence of each type of transport. Most units should move by road, rail should
# be used a little less often than road, ships a bit less often than that, cargo planes
# infrequently, and helicopters rarely. Convoys, trains, and ships make the most
# interesting targets for players (and the easiest to generate AI flight plans for).
class SupplyRoute:
    def __init__(self, control_points: List[ControlPoint]) -> None:
        self.control_points = control_points

    def __contains__(self, item: ControlPoint) -> bool:
        return item in self.control_points

    def __iter__(self) -> Iterator[ControlPoint]:
        yield from self.control_points

    def __len__(self) -> int:
        return len(self.control_points)

    def connections_from(self, control_point: ControlPoint) -> Iterable:
        raise NotImplementedError

    def shortest_path_between(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> List[ControlPoint]:
        if origin not in self:
            raise ValueError(f"{origin} is not in supply route to {destination}")
        if destination not in self:
            raise ValueError(f"{destination} is not in supply route from {origin}")

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
                if current.captured != neighbor.captured:
                    continue

                new_cost = cost + 1
                if new_cost < best_known[neighbor]:
                    best_known[neighbor] = new_cost
                    frontier.push(neighbor, new_cost)
                    came_from[neighbor] = current

        # Reconstruct and reverse the path.
        current = destination
        path: List[ControlPoint] = []
        while current != origin:
            path.append(current)
            previous = came_from[current]
            if previous is None:
                raise RuntimeError(
                    f"Could not reconstruct path to {destination} from {origin}"
                )
            current = previous
        path.reverse()
        return path


class RoadNetwork(SupplyRoute):
    @classmethod
    def for_control_point(cls, control_point: ControlPoint) -> RoadNetwork:
        connected_friendly_points = control_point.transitive_connected_friendly_points()
        if not connected_friendly_points:
            return RoadNetwork([control_point])
        return RoadNetwork([control_point] + connected_friendly_points)

    def connections_from(self, control_point: ControlPoint) -> Iterable:
        yield from control_point.connected_points


class ShippingNetwork(SupplyRoute):
    @classmethod
    def for_control_point(cls, control_point: ControlPoint) -> ShippingNetwork:
        connected_friendly_points = (
            control_point.transitive_friendly_shipping_destinations()
        )
        if not connected_friendly_points:
            return ShippingNetwork([control_point])
        return ShippingNetwork([control_point] + connected_friendly_points)

    def connections_from(self, control_point: ControlPoint) -> Iterable:
        yield from control_point.shipping_lanes
