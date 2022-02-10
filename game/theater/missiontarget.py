from __future__ import annotations

from collections.abc import Sequence
from typing import Iterator, TYPE_CHECKING, Union

from dcs.mapping import Point
from dcs.unit import Unit

if TYPE_CHECKING:
    from game.ato.flighttype import FlightType
    from game.theater import TheaterUnit


class MissionTarget:
    def __init__(self, name: str, position: Point) -> None:
        """Initializes a mission target.

        Args:
            name: The name of the mission target.
            position: The location of the mission target.
        """
        self.name = name
        self.position = position

    def distance_to(self, other: MissionTarget) -> float:
        """Computes the distance to the given mission target."""
        return self.position.distance_to_point(other.position)

    def is_friendly(self, to_player: bool) -> bool:
        """Returns True if the objective is in friendly territory."""
        raise NotImplementedError

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from game.ato import FlightType

        if self.is_friendly(for_player):
            yield FlightType.BARCAP
        else:
            yield from [
                FlightType.ESCORT,
                FlightType.TARCAP,
                FlightType.SEAD_ESCORT,
                FlightType.SWEEP,
                # TODO: FlightType.ELINT,
                # TODO: FlightType.EWAR,
                # TODO: FlightType.RECON,
            ]

    @property
    def strike_targets(self) -> list[TheaterUnit]:
        return []
