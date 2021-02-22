from __future__ import annotations
import random
from typing import TYPE_CHECKING

from dcs.ships import (
    FFL_1124_4_Grisha,
    FSG_1241_1MP_Molniya,
    FFG_11540_Neustrashimy,
    FF_1135M_Rezky,
    CG_1164_Moskva,
    SSK_877,
    SSK_641B,
)

from gen.fleet.dd_group import DDGroupGenerator
from gen.sam.group_generator import ShipGroupGenerator
from game.factions.faction import Faction
from game.theater.theatergroundobject import TheaterGroundObject


if TYPE_CHECKING:
    from game.game import Game


class RussianNavyGroupGenerator(ShipGroupGenerator):
    def generate(self):

        include_frigate = random.choice([True, True, False])
        include_dd = random.choice([True, False])

        if include_dd:
            include_cc = random.choice([True, False])
        else:
            include_cc = False

        if not any([include_frigate, include_dd, include_cc]):
            include_frigate = True

        if include_frigate:
            frigate_type = random.choice([FFL_1124_4_Grisha, FSG_1241_1MP_Molniya])
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
            dd_type = random.choice([FFG_11540_Neustrashimy, FF_1135M_Rezky])
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
            # See https://github.com/Khopa/dcs_liberation/issues/567
            self.add_unit(
                CG_1164_Moskva, "CC1", self.position.x, self.position.y, self.heading
            )

        self.get_generated_group().points[0].speed = 20


class GrishaGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(GrishaGroupGenerator, self).__init__(
            game, ground_object, faction, FFL_1124_4_Grisha
        )


class MolniyaGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(MolniyaGroupGenerator, self).__init__(
            game, ground_object, faction, FSG_1241_1MP_Molniya
        )


class KiloSubGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(KiloSubGroupGenerator, self).__init__(
            game, ground_object, faction, SSK_877
        )


class TangoSubGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(TangoSubGroupGenerator, self).__init__(
            game, ground_object, faction, SSK_641B
        )
