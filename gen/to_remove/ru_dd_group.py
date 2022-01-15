from __future__ import annotations

import random
from typing import TYPE_CHECKING

from dcs.ships import (
    ALBATROS,
    MOLNIYA,
    NEUSTRASH,
    REZKY,
    MOSCOW,
    KILO,
    SOM,
)

from game.factions.faction import Faction
from game.theater.theatergroundobject import ShipGroundObject
from gen.to_remove.dd_group import DDGroupGenerator
from gen.group_generator import ShipGroupGenerator

if TYPE_CHECKING:
    from game.game import Game


class RussianNavyGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:

        self.add_unit(
            ALBATROS,
            "FF1",
            self.position.x + 1200,
            self.position.y + 900,
            self.heading,
        )
        self.add_unit(
            ALBATROS,
            "FF2",
            self.position.x + 1200,
            self.position.y - 900,
            self.heading,
        )

        self.add_unit(
            NEUSTRASH,
            "DD1",
            self.position.x + 2400,
            self.position.y + 900,
            self.heading,
        )
        self.add_unit(
            NEUSTRASH,
            "DD2",
            self.position.x + 2400,
            self.position.y - 900,
            self.heading,
        )

        # Only include the Moskva for now, the Pyotry Velikiy is an unkillable monster.
        # See https://github.com/dcs-liberation/dcs_liberation/issues/567
        self.add_unit(
            MOSCOW,
            "CC1",
            self.position.x,
            self.position.y,
            self.heading,
        )

        self.get_generated_group().points[0].speed = 20


class GrishaGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(GrishaGroupGenerator, self).__init__(
            game, ground_object, faction, ALBATROS
        )


class MolniyaGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(MolniyaGroupGenerator, self).__init__(
            game, ground_object, faction, MOLNIYA
        )


class KiloSubGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(KiloSubGroupGenerator, self).__init__(game, ground_object, faction, KILO)


class TangoSubGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(TangoSubGroupGenerator, self).__init__(game, ground_object, faction, SOM)
