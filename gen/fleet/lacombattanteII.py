from dcs.ships import La_Combattante_II

from game import Game
from game.factions.faction import Faction
from game.theater import TheaterGroundObject
from gen.fleet.dd_group import DDGroupGenerator


class LaCombattanteIIGroupGenerator(DDGroupGenerator):
    def __init__(
        self, game: Game, ground_object: TheaterGroundObject, faction: Faction
    ):
        super(LaCombattanteIIGroupGenerator, self).__init__(
            game, ground_object, faction, La_Combattante_II
        )
