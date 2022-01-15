import random

from dcs.vehicles import Unarmed, MissilesSS, AirDefence

from game import Game
from game.factions.faction import Faction
from game.theater.theatergroundobject import MissileSiteGroundObject
from game.utils import Heading
from gen.group_generator import VehicleGroupGenerator


class ScudGenerator(VehicleGroupGenerator[MissileSiteGroundObject]):
    def __init__(
        self, game: Game, ground_object: MissileSiteGroundObject, faction: Faction
    ) -> None:
        super(ScudGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self) -> None:

        # Scuds
        self.add_unit(
            MissilesSS.Scud_B,
            "V1#0",
            self.position.x,
            self.position.y + random.randint(1, 8),
            self.heading,
        )
        self.add_unit(
            MissilesSS.Scud_B,
            "V1#1",
            self.position.x + 50,
            self.position.y + random.randint(1, 8),
            self.heading,
        )
        self.add_unit(
            MissilesSS.Scud_B,
            "V1#2",
            self.position.x + 100,
            self.position.y + random.randint(1, 8),
            self.heading,
        )

        # Commander
        self.add_unit(
            Unarmed.UAZ_469,
            "Kubel#0",
            self.position.x - 35,
            self.position.y - 20,
            self.heading,
        )

        # Shorad
        self.add_unit(
            AirDefence.ZSU_23_4_Shilka,
            "SHILKA#0",
            self.position.x - 55,
            self.position.y - 38,
            self.heading,
        )

        self.add_unit(
            AirDefence.Strela_1_9P31,
            "STRELA#0",
            self.position.x + 200,
            self.position.y + 15,
            Heading.from_degrees(90),
        )
