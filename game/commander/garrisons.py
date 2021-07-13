from __future__ import annotations

from collections import Iterator
from dataclasses import dataclass

from game.theater import ConflictTheater, ControlPoint
from game.theater.theatergroundobject import VehicleGroupGroundObject
from game.utils import meters, nautical_miles


@dataclass
class Garrisons:
    blocking_capture: list[VehicleGroupGroundObject]
    defending_front_line: list[VehicleGroupGroundObject]
    reserves: list[VehicleGroupGroundObject]

    @property
    def in_priority_order(self) -> Iterator[VehicleGroupGroundObject]:
        yield from self.blocking_capture
        yield from self.defending_front_line
        yield from self.reserves

    def eliminate(self, garrison: VehicleGroupGroundObject) -> None:
        if garrison in self.blocking_capture:
            self.blocking_capture.remove(garrison)
        if garrison in self.defending_front_line:
            self.defending_front_line.remove(garrison)
        if garrison in self.reserves:
            self.reserves.remove(garrison)

    def __contains__(self, item: VehicleGroupGroundObject) -> bool:
        return item in self.in_priority_order

    @classmethod
    def from_theater(cls, theater: ConflictTheater, player_owned: bool) -> Garrisons:
        """Categorize garrison groups based on target priority.

        Any garrisons blocking base capture are the highest priority, followed by other
        garrisons at front-line bases, and finally any garrisons in reserve at other
        bases.
        """
        blocking = []
        defending = []
        reserves = []
        for cp in theater.control_points_for(player_owned):
            garrisons = [
                tgo
                for tgo in cp.ground_objects
                if isinstance(tgo, VehicleGroupGroundObject) and not tgo.is_dead
            ]
            if not cp.has_active_frontline:
                reserves.extend(garrisons)
                continue

            for garrison in garrisons:
                if meters(garrison.distance_to(cp)) < ControlPoint.CAPTURE_DISTANCE:
                    blocking.append(garrison)
                else:
                    defending.append(garrison)

        return Garrisons(blocking, defending, reserves)
