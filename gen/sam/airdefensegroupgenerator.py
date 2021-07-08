from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterator, List

from dcs.unitgroup import VehicleGroup

from game import Game
from game.theater.theatergroundobject import SamGroundObject
from gen.sam.group_generator import GroupGenerator


class SkynetRole(Enum):
    #: A radar SAM that should be controlled by Skynet.
    Sam = "Sam"

    #: A radar SAM that should be controlled and used as an EWR by Skynet.
    SamAsEwr = "SamAsEwr"

    #: An air defense unit that should be used as point defense by Skynet.
    PointDefense = "PD"

    #: All other types of groups that might be present in a SAM TGO. This includes
    #: SHORADS, AAA, supply trucks, etc. Anything that shouldn't be controlled by Skynet
    #: should use this role.
    NoSkynetBehavior = "NoSkynetBehavior"


class AirDefenseRange(Enum):
    AAA = ("AAA", SkynetRole.NoSkynetBehavior)
    Short = ("short", SkynetRole.NoSkynetBehavior)
    Medium = ("medium", SkynetRole.Sam)
    Long = ("long", SkynetRole.SamAsEwr)

    def __init__(self, description: str, default_role: SkynetRole) -> None:
        self.range_name = description
        self.default_role = default_role


class AirDefenseGroupGenerator(GroupGenerator[VehicleGroup], ABC):
    """
    This is the base for all SAM group generators
    """

    def __init__(self, game: Game, ground_object: SamGroundObject) -> None:
        super().__init__(game, ground_object)

        self.vg.name = self.group_name_for_role(self.vg.id, self.primary_group_role())
        self.auxiliary_groups: List[VehicleGroup] = []

    def add_auxiliary_group(self, role: SkynetRole) -> VehicleGroup:
        gid = self.game.next_group_id()
        group = VehicleGroup(gid, self.group_name_for_role(gid, role))
        self.auxiliary_groups.append(group)
        return group

    def group_name_for_role(self, gid: int, role: SkynetRole) -> str:
        if role is SkynetRole.NoSkynetBehavior:
            # No special naming needed for air defense groups that don't participate in
            # Skynet.
            return f"{self.go.group_name}|{gid}"

        # For those that do, we need a prefix of `$COLOR|SAM| so our Skynet config picks
        # the group up at all. To support PDs we need to append the ID of the TGO so
        # that the PD will know which group it's protecting. We then append the role so
        # our config knows what to do with the group, and finally the GID of *this*
        # group to ensure no conflicts.
        return "|".join(
            [self.go.faction_color, "SAM", str(self.go.group_id), role.value, str(gid)]
        )

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
    def primary_group_role(cls) -> SkynetRole:
        return cls.range().default_role
