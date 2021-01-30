from __future__ import annotations
from typing import TYPE_CHECKING

from game.factions.faction import Faction
from game.theater.theatergroundobject import TheaterGroundObject

from gen.sam.group_generator import ShipGroupGenerator
from dcs.unittype import ShipType
from dcs.ships import Ticonderoga_class

if TYPE_CHECKING:
    from game.game import Game


class CCGroupGenerator(ShipGroupGenerator):

    def __init__(self, game: Game, ground_object: TheaterGroundObject, faction: Faction, cctype: ShipType):
        super(CCGroupGenerator, self).__init__(game, ground_object, faction)
        self.cctype = cctype

    def generate(self):
        self.add_unit(self.cctype, "CC1", self.position.x + 500, self.position.y + 900, self.heading)
        self.add_unit(self.cctype, "CC2", self.position.x + 500, self.position.y - 900, self.heading)
        self.get_generated_group().points[0].speed = 20


class TiconderogaGroupGenerator(CCGroupGenerator):
    def __init__(self, game: Game, ground_object: TheaterGroundObject, faction: Faction):
        super(TiconderogaGroupGenerator, self).__init__(game, ground_object, faction, Ticonderoga_class)