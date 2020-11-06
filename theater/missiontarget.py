from __future__ import annotations

from dcs.mapping import Point


class MissionTarget:
    def __init__(self, name: str, position: Point) -> None:
        """Initializes a mission target.

        Args:
            name: The name of the mission target.
            position: The location of the mission target.
        """
        self.name = name
        self.position = position

    def distance_to(self, other: MissionTarget) -> int:
        """Computes the distance to the given mission target."""
        return self.position.distance_to_point(other.position)
