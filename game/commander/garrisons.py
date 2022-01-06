from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from game.theater import ControlPoint
from game.theater.theatergroundobject import VehicleGroupGroundObject
from game.utils import meters


@dataclass
class Garrisons:
    blocking_capture: list[VehicleGroupGroundObject]
    defending_front_line: list[VehicleGroupGroundObject]

    @property
    def in_priority_order(self) -> Iterator[VehicleGroupGroundObject]:
        yield from self.blocking_capture
        yield from self.defending_front_line

    def eliminate(self, garrison: VehicleGroupGroundObject) -> None:
        if garrison in self.blocking_capture:
            self.blocking_capture.remove(garrison)
        if garrison in self.defending_front_line:
            self.defending_front_line.remove(garrison)

    def __contains__(self, item: VehicleGroupGroundObject) -> bool:
        return item in self.in_priority_order

    @classmethod
    def for_control_point(cls, control_point: ControlPoint) -> Garrisons:
        """Categorize garrison groups based on target priority.

        Any garrisons blocking base capture are the highest priority.
        """
        blocking = []
        defending = []
        garrisons = [
            tgo
            for tgo in control_point.ground_objects
            if isinstance(tgo, VehicleGroupGroundObject) and not tgo.is_dead
        ]
        for garrison in garrisons:
            if (
                meters(garrison.distance_to(control_point))
                < ControlPoint.CAPTURE_DISTANCE
            ):
                blocking.append(garrison)
            else:
                defending.append(garrison)

        return Garrisons(blocking, defending)
