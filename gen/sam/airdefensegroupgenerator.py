from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, List

from dcs.unitgroup import VehicleGroup

from game import Game
from game.theater.theatergroundobject import SamGroundObject, AirDefenseRange
from gen.sam.group_generator import GroupGenerator


class AirDefenseGroupGenerator(GroupGenerator, ABC):
    """
    This is the base for all SAM group generators
    """

    price: int

    def __init__(self, game: Game, ground_object: SamGroundObject) -> None:
        super().__init__(game, ground_object)

        self.auxiliary_groups: List[VehicleGroup] = []
        self.auxiliary_ranges: List[AirDefenseRange] = []

    def add_auxiliary_group(self, aa_range: AirDefenseRange) -> VehicleGroup:
        group = VehicleGroup(
            self.game.next_group_id(), "|".join([self.go.group_name, aa_range.value])
        )
        self.auxiliary_groups.append(group)
        self.auxiliary_ranges.append(aa_range)
        return group

    def get_generated_group(self) -> VehicleGroup:
        raise RuntimeError(
            "Deprecated call to AirDefenseGroupGenerator.get_generated_group "
            "misses auxiliary groups. Use AirDefenseGroupGenerator.groups "
            "instead."
        )

    @property
    def groups(self) -> Iterator[VehicleGroup]:
        yield self.vg
        yield from self.auxiliary_groups

    @property
    def ranges(self) -> Iterator[AirDefenseRange]:
        yield self.range()
        yield from self.auxiliary_ranges

    @classmethod
    @abstractmethod
    def range(cls) -> AirDefenseRange:
        ...
