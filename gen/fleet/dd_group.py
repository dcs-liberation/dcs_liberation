from __future__ import annotations
from typing import TYPE_CHECKING

from game.factions.faction import Faction
from theater.theatergroundobject import TheaterGroundObject

from gen.sam.group_generator import ShipGroupGenerator
from dcs.unittype import ShipType
from dcs.ships import Oliver_Hazzard_Perry_class, USS_Arleigh_Burke_IIa

if TYPE_CHECKING:
    from game.game import Game


class DDGroupGenerator(ShipGroupGenerator):

    def __init__(self, game: Game, ground_object: TheaterGroundObject, faction: Faction, ddtype: ShipType):
        super(DDGroupGenerator, self).__init__(game, ground_object, faction)
        self.ddtype = ddtype

    def generate(self):
        self.add_unit(self.ddtype, "DD1", self.position.x + 500, self.position.y + 900, self.heading)
        self.add_unit(self.ddtype, "DD2", self.position.x + 500, self.position.y - 900, self.heading)
        self.get_generated_group().points[0].speed = 20


class OliverHazardPerryGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: TheaterGroundObject, faction: Faction):
        super(OliverHazardPerryGroupGenerator, self).__init__(game, ground_object, faction, Oliver_Hazzard_Perry_class)


class ArleighBurkeGroupGenerator(DDGroupGenerator):
    def __init__(self, game: Game, ground_object: TheaterGroundObject, faction: Faction):
        super(ArleighBurkeGroupGenerator, self).__init__(game, ground_object, faction, USS_Arleigh_Burke_IIa)
