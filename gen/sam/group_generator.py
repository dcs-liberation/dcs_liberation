from __future__ import annotations

import logging
import math
import operator
import random
from collections import Iterable
from typing import TYPE_CHECKING, Type, TypeVar, Generic, Any

from dcs import unitgroup
from dcs.mapping import Point
from dcs.point import PointAction
from dcs.unit import Ship, Vehicle, Unit
from dcs.unitgroup import ShipGroup, VehicleGroup
from dcs.unittype import VehicleType, UnitType, ShipType

from game.dcs.groundunittype import GroundUnitType
from game.factions.faction import Faction
from game.theater import MissionTarget
from game.theater.theatergroundobject import TheaterGroundObject, NavalGroundObject
from game.utils import Heading

if TYPE_CHECKING:
    from game.game import Game


GroupT = TypeVar("GroupT", VehicleGroup, ShipGroup)
UnitT = TypeVar("UnitT", bound=Unit)
UnitTypeT = TypeVar("UnitTypeT", bound=Type[UnitType])
TgoT = TypeVar("TgoT", bound=TheaterGroundObject[Any])


# TODO: Generate a group description rather than a pydcs group.
# It appears that all of this work gets redone at miz generation time (see
# groundobjectsgen for an example). We can do less work and include the data we
# care about in the format we want if we just generate our own group description
# types rather than pydcs groups.
class GroupGenerator(Generic[GroupT, UnitT, UnitTypeT, TgoT]):
    def __init__(self, game: Game, ground_object: TgoT, group: GroupT) -> None:
        self.game = game
        self.go = ground_object
        self.position = ground_object.position
        self.heading: Heading = Heading.random()
        self.price = 0
        self.vg: GroupT = group

    def generate(self) -> None:
        raise NotImplementedError

    def get_generated_group(self) -> GroupT:
        return self.vg

    def add_unit(
        self,
        unit_type: UnitTypeT,
        name: str,
        pos_x: float,
        pos_y: float,
        heading: Heading,
    ) -> UnitT:
        return self.add_unit_to_group(
            self.vg, unit_type, name, Point(pos_x, pos_y), heading
        )

    def add_unit_to_group(
        self,
        group: GroupT,
        unit_type: UnitTypeT,
        name: str,
        position: Point,
        heading: Heading,
    ) -> UnitT:
        raise NotImplementedError

    def heading_to_conflict(self) -> int:
        # Heading for a Group to the enemy.
        # Should be the point between the nearest and the most distant conflict
        conflicts: dict[MissionTarget, float] = {}

        for conflict in self.game.theater.conflicts():
            conflicts[conflict] = conflict.distance_to(self.go)

        if len(conflicts) == 0:
            return self.heading

        closest_conflict = min(conflicts.items(), key=operator.itemgetter(1))[0]
        most_distant_conflict = max(conflicts.items(), key=operator.itemgetter(1))[0]

        conflict_center = Point(
            (closest_conflict.position.x + most_distant_conflict.position.x) / 2,
            (closest_conflict.position.y + most_distant_conflict.position.y) / 2,
        )

        return int(self.go.position.heading_between_point(conflict_center))


class VehicleGroupGenerator(
    Generic[TgoT], GroupGenerator[VehicleGroup, Vehicle, Type[VehicleType], TgoT]
):
    def __init__(self, game: Game, ground_object: TgoT) -> None:
        super().__init__(
            game,
            ground_object,
            unitgroup.VehicleGroup(game.next_group_id(), ground_object.group_name),
        )
        wp = self.vg.add_waypoint(self.position, PointAction.OffRoad, 0)
        wp.ETA_locked = True

    def generate(self) -> None:
        raise NotImplementedError

    def add_unit_to_group(
        self,
        group: VehicleGroup,
        unit_type: Type[VehicleType],
        name: str,
        position: Point,
        heading: Heading,
    ) -> Vehicle:
        unit = Vehicle(self.game.next_unit_id(), f"{group.name}|{name}", unit_type.id)
        unit.position = position
        unit.heading = heading.degrees
        group.add_unit(unit)

        # get price of unit to calculate the real price of the whole group
        try:
            ground_unit_type = next(GroundUnitType.for_dcs_type(unit_type))
            self.price += ground_unit_type.price
        except StopIteration:
            logging.error(f"Cannot get price for unit {unit_type.name}")

        return unit

    def get_circular_position(
        self, num_units: int, launcher_distance: int, coverage: int = 90
    ) -> Iterable[tuple[float, float, Heading]]:
        """
        Given a position on the map, array a group of units in a circle a uniform distance from the unit
        :param num_units:
            number of units to play on the circle
        :param launcher_distance:
            distance the units should be from the center unit
        :param coverage:
            0-360
        :return:
            list of tuples representing each unit location
                [(pos_x, pos_y, heading), ...]
        """
        if coverage == 360:
            # one of the positions is shared :'(
            outer_offset = coverage / num_units
        else:
            outer_offset = coverage / (num_units - 1)

        positions = []

        if num_units % 2 == 0:
            current_offset = self.heading.degrees - ((coverage / (num_units - 1)) / 2)
        else:
            current_offset = self.heading.degrees
        current_offset -= outer_offset * (math.ceil(num_units / 2) - 1)
        for _ in range(1, num_units + 1):
            x: float = self.position.x + launcher_distance * math.cos(
                math.radians(current_offset)
            )
            y: float = self.position.y + launcher_distance * math.sin(
                math.radians(current_offset)
            )
            positions.append((x, y, Heading.from_degrees(current_offset)))
            current_offset += outer_offset
        return positions


class ShipGroupGenerator(
    GroupGenerator[ShipGroup, Ship, Type[ShipType], NavalGroundObject]
):
    """Abstract class for other ship generator classes"""

    def __init__(self, game: Game, ground_object: NavalGroundObject, faction: Faction):
        super().__init__(
            game,
            ground_object,
            unitgroup.ShipGroup(game.next_group_id(), ground_object.group_name),
        )
        self.faction = faction
        wp = self.vg.add_waypoint(self.position, 0)
        wp.ETA_locked = True

    def generate(self) -> None:
        raise NotImplementedError

    def add_unit_to_group(
        self,
        group: ShipGroup,
        unit_type: Type[ShipType],
        name: str,
        position: Point,
        heading: Heading,
    ) -> Ship:
        unit = Ship(self.game.next_unit_id(), f"{self.go.group_name}|{name}", unit_type)
        unit.position = position
        unit.heading = heading.degrees
        group.add_unit(unit)
        return unit
