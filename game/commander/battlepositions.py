from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from game.theater import ControlPoint
from game.theater.theatergroundobject import VehicleGroupGroundObject
from game.utils import meters


@dataclass
class BattlePositions:
    blocking_capture: list[VehicleGroupGroundObject]
    defending_front_line: list[VehicleGroupGroundObject]

    @property
    def in_priority_order(self) -> Iterator[VehicleGroupGroundObject]:
        yield from self.blocking_capture
        yield from self.defending_front_line

    def eliminate(self, battle_position: VehicleGroupGroundObject) -> None:
        if battle_position in self.blocking_capture:
            self.blocking_capture.remove(battle_position)
        if battle_position in self.defending_front_line:
            self.defending_front_line.remove(battle_position)

    def __contains__(self, item: VehicleGroupGroundObject) -> bool:
        return item in self.in_priority_order

    @classmethod
    def for_control_point(cls, control_point: ControlPoint) -> BattlePositions:
        """Categorize battle position groups based on target priority.

        Any battle positions blocking base capture are the highest priority.
        """
        blocking = []
        defending = []
        battle_positions = [
            tgo
            for tgo in control_point.ground_objects
            if isinstance(tgo, VehicleGroupGroundObject) and not tgo.is_dead
        ]
        for battle_position in battle_positions:
            if (
                meters(battle_position.distance_to(control_point))
                < ControlPoint.CAPTURE_DISTANCE
            ):
                blocking.append(battle_position)
            else:
                defending.append(battle_position)

        return BattlePositions(blocking, defending)
