from __future__ import annotations

import heapq
import math
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional

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


class SupplyRoute:
    def __init__(self, control_points: List[ControlPoint]) -> None:
        self.control_points = control_points

    def __contains__(self, item: ControlPoint) -> bool:
        return item in self.control_points

    def __iter__(self) -> Iterator[ControlPoint]:
        yield from self.control_points

    def __len__(self) -> int:
        return len(self.control_points)

    @classmethod
    def for_control_point(cls, control_point: ControlPoint) -> SupplyRoute:
        connected_friendly_points = control_point.transitive_connected_friendly_points()
        if not connected_friendly_points:
            return SupplyRoute([control_point])
        return SupplyRoute([control_point] + connected_friendly_points)

    def shortest_path_between(
        self, origin: ControlPoint, destination: ControlPoint
    ) -> List[ControlPoint]:
        if origin not in self:
            raise ValueError(f"{origin.name} is not in this supply route")
        if destination not in self:
            raise ValueError(f"{destination.name} is not in this supply route")

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

            for neighbor in current.connected_points:
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
