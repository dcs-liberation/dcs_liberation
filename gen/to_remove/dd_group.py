from __future__ import annotations

from typing import TYPE_CHECKING, Type

from dcs.ships import PERRY, USS_Arleigh_Burke_IIa
from dcs.unittype import ShipType

from game.factions.faction import Faction
from game.theater.theatergroundobject import ShipGroundObject
from gen.group_generator import ShipGroupGenerator

if TYPE_CHECKING:
    from game.game import Game


class DDGroupGenerator(ShipGroupGenerator):
    def __init__(
        self,
        game: Game,
        ground_object: ShipGroundObject,
        faction: Faction,
        ddtype: Type[ShipType],
    ):
        super(DDGroupGenerator, self).__init__(game, ground_object, faction)
        self.ddtype = ddtype

    def generate(self) -> None:
        self.add_unit(
            self.ddtype,
            "DD1",
            self.position.x + 500,
            self.position.y + 900,
            self.heading,
        )
        self.add_unit(
            self.ddtype,
            "DD2",
            self.position.x + 500,
            self.position.y - 900,
            self.heading,
        )
        self.get_generated_group().points[0].speed = 20


class OliverHazardPerryGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(OliverHazardPerryGroupGenerator, self).__init__(
            game, ground_object, faction, PERRY
        )


class ArleighBurkeGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: ShipGroundObject, faction: Faction):
        super(ArleighBurkeGroupGenerator, self).__init__(
            game, ground_object, faction, USS_Arleigh_Burke_IIa
        )
