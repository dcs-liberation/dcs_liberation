from __future__ import annotations

from typing import Iterator, List, Optional

from game.theater.controlpoint import ControlPoint


class SupplyRoute:
    def __init__(self, control_points: List[ControlPoint]) -> None:
        self.control_points = control_points

    def __contains__(self, item: ControlPoint) -> bool:
        return item in self.control_points

    def __iter__(self) -> Iterator[ControlPoint]:
        yield from self.control_points

    @classmethod
    def for_control_point(cls, control_point: ControlPoint) -> Optional[SupplyRoute]:
        connected_friendly_points = control_point.transitive_connected_friendly_points()
        if not connected_friendly_points:
            return None
        return SupplyRoute([control_point] + connected_friendly_points)
