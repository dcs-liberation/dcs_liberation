from __future__ import annotations

import random
from typing import TYPE_CHECKING


from dcs.ships import (
    Type_052C_Destroyer,
    Type_052B_Destroyer,
    Type_054A_Frigate,
)

from game.factions.faction import Faction
from gen.fleet.dd_group import DDGroupGenerator
from gen.sam.group_generator import ShipGroupGenerator
from game.theater.theatergroundobject import TheaterGroundObject

if TYPE_CHECKING:
    from game.game import Game


class ChineseNavyGroupGenerator(ShipGroupGenerator):
    def generate(self):

        include_frigate = random.choice([True, True, False])
        include_dd = random.choice([True, False])

        if not any([include_frigate, include_dd]):
            include_frigate = True

        if include_frigate:
            self.add_unit(
                Type_054A_Frigate,
                "FF1",
                self.position.x + 1200,
                self.position.y + 900,
                self.heading,
            )
            self.add_unit(
                Type_054A_Frigate,
                "FF2",
                self.position.x + 1200,
                self.position.y - 900,
                self.heading,
            )

        if include_dd:
            dd_type = random.choice([Type_052C_Destroyer, Type_052B_Destroyer])
            self.add_unit(
                dd_type,
                "DD1",
                self.position.x + 2400,
                self.position.y + 900,
                self.heading,
            )
            self.add_unit(
                dd_type,
                "DD2",
                self.position.x + 2400,
                self.position.y - 900,
                self.heading,
            )

        self.get_generated_group().points[0].speed = 20


class Type54GroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(Type54GroupGenerator, self).__init__(
            game, ground_object, faction, Type_054A_Frigate
        )
