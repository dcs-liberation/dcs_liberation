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

from gen.fleet.dd_group import DDGroupGenerator
from gen.sam.group_generator import ShipGroupGenerator
from game.factions.faction import Faction
from game.theater.theatergroundobject import TheaterGroundObject


if TYPE_CHECKING:
    from game.game import Game


class RussianNavyGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:

        include_frigate = random.choice([True, True, False])
        include_dd = random.choice([True, False])

        if include_dd:
            include_cc = random.choice([True, False])
        else:
            include_cc = False

        if not any([include_frigate, include_dd, include_cc]):
            include_frigate = True

        if include_frigate:
            frigate_type = random.choice([ALBATROS, MOLNIYA])
            self.add_unit(
                frigate_type,
                "FF1",
                self.position.x + 1200,
                self.position.y + 900,
                self.heading,
            )
            self.add_unit(
                frigate_type,
                "FF2",
                self.position.x + 1200,
                self.position.y - 900,
                self.heading,
            )

        if include_dd:
            dd_type = random.choice([NEUSTRASH, REZKY])
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

        if include_cc:
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
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(GrishaGroupGenerator, self).__init__(
            game, ground_object, faction, ALBATROS
        )


class MolniyaGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(MolniyaGroupGenerator, self).__init__(
            game, ground_object, faction, MOLNIYA
        )


class KiloSubGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(KiloSubGroupGenerator, self).__init__(game, ground_object, faction, KILO)


class TangoSubGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(TangoSubGroupGenerator, self).__init__(game, ground_object, faction, SOM)
