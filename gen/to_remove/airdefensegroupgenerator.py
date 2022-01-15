from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator, List

from dcs.unitgroup import VehicleGroup

from game import Game
from game.theater.theatergroundobject import (
    SamGroundObject,
    SkynetRole,
    AirDefenseRange,
)
from gen.group_generator import VehicleGroupGenerator


class AirDefenseGroupGenerator(VehicleGroupGenerator[SamGroundObject], ABC):
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
        return "|".join([self.go.faction_color, "SAM", role.value, str(gid)])

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
