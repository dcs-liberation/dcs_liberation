from __future__ import annotations

from typing import TypeVar

from dcs.mapping import Point
from dcs.unitgroup import StaticGroup, ShipGroup, VehicleGroup

from game.point_with_heading import PointWithHeading
from game.utils import Heading

GroupT = TypeVar("GroupT", StaticGroup, ShipGroup, VehicleGroup)


class PresetLocation(PointWithHeading):
    """Store information about the Preset Location set by the campaign designer"""

    # This allows to store original name and force a specific type or template
    original_name: str  # Store the original name from the campaign miz

    def __init__(
        self, name: str, position: Point, heading: Heading = Heading.from_degrees(0)
    ) -> None:
        super().__init__(position.x, position.y, heading, position._terrain)
        self.original_name = name

    @classmethod
    def from_group(cls, group: GroupT) -> PresetLocation:
        """Creates a PresetLocation from a placeholder group in the campaign miz"""
        preset = PresetLocation(
            group.name,
            group.position,
            Heading.from_degrees(group.units[0].heading),
        )
        return preset
