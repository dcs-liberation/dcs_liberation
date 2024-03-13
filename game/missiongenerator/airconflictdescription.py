from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.theater import ConflictTheater, ControlPoint


class AirConflictDescription:
    def __init__(self, blue_cp: ControlPoint, red_cp: ControlPoint) -> None:
        self.blue_cp = blue_cp
        self.red_cp = red_cp
        self.center = (self.blue_cp.position + self.red_cp.position) / 2

    @staticmethod
    def for_theater(theater: ConflictTheater) -> AirConflictDescription:
        player_cp, enemy_cp = theater.closest_opposing_control_points()
        return AirConflictDescription(player_cp, enemy_cp)
