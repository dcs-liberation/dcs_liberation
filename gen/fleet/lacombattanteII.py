from dcs.ships import FAC_La_Combattante_IIa

from game.factions.faction import Faction
from game.theater import TheaterGroundObject
from gen.fleet.dd_group import DDGroupGenerator


class LaCombattanteIIGroupGenerator(DDGroupGenerator):
    def __init__(self, game, ground_object: TheaterGroundObject, faction: Faction):
        super(LaCombattanteIIGroupGenerator, self).__init__(
            game, ground_object, faction, FAC_La_Combattante_IIa
        )
