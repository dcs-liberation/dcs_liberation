"""Objective adjacency lists."""
from __future__ import annotations

from typing import Dict, Iterator, List, Optional, TYPE_CHECKING

from game.utils import Distance

if TYPE_CHECKING:
    from game.theater import ConflictTheater, ControlPoint, MissionTarget


class ClosestAirfields:
    """Precalculates which control points are closes to the given target."""

    def __init__(
        self, target: MissionTarget, all_control_points: List[ControlPoint]
    ) -> None:
        self.target = target
        # This cache is configured once on load, so it's important that it is
        # complete and deterministic to avoid different behaviors across loads.
        # E.g. https://github.com/dcs-liberation/dcs_liberation/issues/819
        self.closest_airfields: List[ControlPoint] = sorted(
            all_control_points, key=lambda c: self.target.distance_to(c)
        )

    @property
    def operational_airfields(self) -> Iterator[ControlPoint]:
        return (c for c in self.closest_airfields if c.runway_is_operational())

    def _airfields_within(
        self, distance: Distance, operational: bool
    ) -> Iterator[ControlPoint]:
        airfields = (
            self.operational_airfields if operational else self.closest_airfields
        )
        for cp in airfields:
            if cp.distance_to(self.target) < distance.meters:
                yield cp
            else:
                break

    def operational_airfields_within(
        self, distance: Distance
    ) -> Iterator[ControlPoint]:
        """Iterates over all airfields within the given range of the target.

        Note that this iterates over *all* airfields, not just friendly
        airfields.
        """
        return self._airfields_within(distance, operational=True)

    def all_airfields_within(self, distance: Distance) -> Iterator[ControlPoint]:
        """Iterates over all airfields within the given range of the target.

        Note that this iterates over *all* airfields, not just friendly
        airfields.
        """
        return self._airfields_within(distance, operational=False)


class ObjectiveDistanceCache:
    theater: Optional[ConflictTheater] = None
    closest_airfields: Dict[str, ClosestAirfields] = {}

    @classmethod
    def set_theater(cls, theater: ConflictTheater) -> None:
        if cls.theater is not None:
            cls.closest_airfields = {}
        cls.theater = theater

    @classmethod
    def get_closest_airfields(cls, location: MissionTarget) -> ClosestAirfields:
        if cls.theater is None:
            raise RuntimeError("Call ObjectiveDistanceCache.set_theater before using")

        if location.name not in cls.closest_airfields:
            cls.closest_airfields[location.name] = ClosestAirfields(
                location, cls.theater.controlpoints
            )
        return cls.closest_airfields[location.name]
