from __future__ import annotations

import random
from typing import TYPE_CHECKING

from dcs.ships import (
    Type_052C,
    Type_052B,
    Type_054A,
)

from game.factions.faction import Faction
from game.theater.theatergroundobject import ShipGroundObject
from gen.to_remove.dd_group import DDGroupGenerator
from gen.group_generator import ShipGroupGenerator

if TYPE_CHECKING:
    from game.game import Game


class ChineseNavyGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:
        self.add_unit(
            Type_054A,
            "FF1",
            self.position.x + 1200,
            self.position.y + 900,
            self.heading,
        )
        self.add_unit(
            Type_054A,
            "FF2",
            self.position.x + 1200,
            self.position.y - 900,
            self.heading,
        )
        self.add_unit(
            Type_052C,
            "DD1",
            self.position.x + 2400,
            self.position.y + 900,
            self.heading,
        )
        self.add_unit(
            Type_052C,
            "DD2",
            self.position.x + 2400,
            self.position.y - 900,
            self.heading,
        )

        self.get_generated_group().points[0].speed = 20


class Type54GroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(Type54GroupGenerator, self).__init__(
            game, ground_object, faction, Type_054A
        )