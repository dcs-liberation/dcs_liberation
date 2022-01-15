import random

from dcs.vehicles import Unarmed, MissilesSS, AirDefence

from game import Game
from game.factions.faction import Faction
from game.theater.theatergroundobject import MissileSiteGroundObject
from game.utils import Heading
from gen.group_generator import VehicleGroupGenerator


class V1GroupGenerator(VehicleGroupGenerator[MissileSiteGroundObject]):
    def __init__(
        self, game: Game, ground_object: MissileSiteGroundObject, faction: Faction
    ) -> None:
        super(V1GroupGenerator, self).__init__(game, ground_object)
        self.faction = faction

    def generate(self) -> None:

        # Ramps
        self.add_unit(
            MissilesSS.V1_launcher,
            "V1#0",
            self.position.x,
            self.position.y + random.randint(1, 8),
            self.heading,
        )
        self.add_unit(
            MissilesSS.V1_launcher,
            "V1#1",
            self.position.x + 50,
            self.position.y + random.randint(1, 8),
            self.heading,
        )
        self.add_unit(
            MissilesSS.V1_launcher,
            "V1#2",
            self.position.x + 100,
            self.position.y + random.randint(1, 8),
            self.heading,
        )

        # Commander
        self.add_unit(
            Unarmed.Kubelwagen_82,
            "Kubel#0",
            self.position.x - 35,
            self.position.y - 20,
            self.heading,
        )

        # Self defense flak
        flak_unit = random.choice([AirDefence.Flak38, AirDefence.Flak30])

        self.add_unit(
            flak_unit,
            "FLAK#0",
            self.position.x - 55,
            self.position.y - 38,
            self.heading,
        )

        self.add_unit(
            Unarmed.Blitz_36_6700A,
            "Blitz#0",
            self.position.x + 200,
            self.position.y + 15,
            Heading.from_degrees(90),
        )
