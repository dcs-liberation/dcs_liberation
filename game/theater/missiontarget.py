from __future__ import annotations

from typing import Iterator, TYPE_CHECKING

from dcs.mapping import Point

if TYPE_CHECKING:
    from gen.flights.flight import FlightType


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

    def is_friendly(self, to_player: bool) -> bool:
        """Returns True if the objective is in friendly territory."""
        raise NotImplementedError

    def mission_types(self, for_player: bool) -> Iterator[FlightType]:
        from gen.flights.flight import FlightType
        if self.is_friendly(for_player):
            yield from [
                FlightType.BARCAP,
                FlightType.AWACS,
            ]
        else:
            yield from [
                FlightType.ESCORT,
                FlightType.AWACS,
                FlightType.TARCAP,
                FlightType.SEAD,
                FlightType.SWEEP,
                # TODO: FlightType.ELINT,
                # TODO: FlightType.EWAR,
                # TODO: FlightType.RECON,
            ]
