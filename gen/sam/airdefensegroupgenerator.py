from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, List

from dcs.unitgroup import VehicleGroup

from game import Game
from game.theater.theatergroundobject import SamGroundObject, IADSRole
from gen.sam.group_generator import VehicleGroupGenerator


class AirDefenseRange(Enum):
    AAA = ("AAA", IADSRole.NoBehavior)
    Short = ("short", IADSRole.NoBehavior)
    Medium = ("medium", IADSRole.Sam)
    Long = ("long", IADSRole.SamAsEwr)

    def __init__(self, description: str, default_role: IADSRole) -> None:
        self.range_name = description
        self.default_role = default_role


class AirDefenseGroupGenerator(VehicleGroupGenerator[SamGroundObject], ABC):
    """
    This is the base for all SAM group generators
    """

    def __init__(self, game: Game, ground_object: SamGroundObject) -> None:
        super().__init__(game, ground_object)

        self.iads_roles: List[IADSRole] = [self.range().default_role]
        self.auxiliary_groups: List[VehicleGroup] = []
        self.heading = self.heading_to_conflict()

    def add_auxiliary_group(self, role: IADSRole) -> VehicleGroup:
        gid = self.game.next_group_id()
        group = VehicleGroup(gid, f"{self.go.group_name}|{role.value}")
        self.auxiliary_groups.append(group)
        self.iads_roles.append(role)
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

    @classmethod
    def primary_group_role(cls) -> IADSRole:
        return cls.range().default_role
