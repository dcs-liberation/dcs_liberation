from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, List

from dcs.unitgroup import VehicleGroup

from game import Game
from game.theater.theatergroundobject import SamGroundObject
from gen.sam.group_generator import GroupGenerator


class AirDefenseRange(Enum):
    AAA = "AAA"
    Short = "short"
    Medium = "medium"
    Long = "long"


class AirDefenseGroupGenerator(GroupGenerator, ABC):
    """
    This is the base for all SAM group generators
    """

    def __init__(self, game: Game, ground_object: SamGroundObject) -> None:
        ground_object.skynet_capable = True
        super().__init__(game, ground_object)

        self.auxiliary_groups: List[VehicleGroup] = []

    def add_auxiliary_group(self, name_suffix: str) -> VehicleGroup:
        group = VehicleGroup(
            self.game.next_group_id(), "|".join([self.go.group_name, name_suffix])
        )
        self.auxiliary_groups.append(group)
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

    @classmethod
    @abstractmethod
    def range(cls) -> AirDefenseRange:
        ...
