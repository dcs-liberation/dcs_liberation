from __future__ import annotations

from abc import ABC, abstractmethod
from dcs.mapping import Point


class MissionTarget(ABC):
    # TODO: These should just be required objects to the constructor
    # The TheatherGroundObject class is difficult to modify because it's
    # generated data that's pickled ahead of time.
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the mission target."""

    @property
    @abstractmethod
    def position(self) -> Point:
        """The location of the mission target."""

    def distance_to(self, other: MissionTarget) -> int:
        """Computes the distance to the given mission target."""
        return self.position.distance_to_point(other.position)
