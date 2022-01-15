import random

from dcs import Point

from gen.group_generator import ShipGroupGenerator
from game.utils import Heading

from dcs.ships import USS_Arleigh_Burke_IIa, TICONDEROG


class CarrierGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:
        if len(self.faction.aircraft_carrier) > 0:
            carrier_type = random.choice(self.faction.aircraft_carrier)
            self.add_unit(
                carrier_type,
                "Carrier",
                self.position.x,
                self.position.y,
                self.heading,
            )
        else:
            return

        aux_group = self.add_auxiliary_group()
        # Add destroyers escort
        if len(self.faction.destroyers) > 0:
            dd_type = random.choice(self.faction.destroyers)
            self.add_unit_to_group(
                aux_group,
                dd_type,
                "DD1",
                Point(self.position.x + 2500, self.position.y + 4500),
                self.heading,
            )
            self.add_unit_to_group(
                aux_group,
                dd_type,
                "DD2",
                Point(self.position.x + 2500, self.position.y - 4500),
                self.heading,
            )

            self.add_unit_to_group(
                aux_group,
                dd_type,
                "DD3",
                Point(self.position.x + 4500, self.position.y + 8500),
                self.heading,
            )
            self.add_unit_to_group(
                aux_group,
                dd_type,
                "DD4",
                Point(self.position.x + 4500, self.position.y - 8500),
                self.heading,
            )

        self.get_generated_group().points[0].speed = 20


class CarrierStrikeGroup8Generator(ShipGroupGenerator):
    def generate(self) -> None:
        # Carrier Strike Group 8
        carrier_type = random.choice(self.faction.aircraft_carrier)

        self.add_unit(
            carrier_type,
            "CVN-75 Harry S. Truman",
            self.position.x,
            self.position.y,
            self.heading,
        )

        aux_group = self.add_auxiliary_group()

        # Add Arleigh Burke escort
        self.add_unit_to_group(
            aux_group,
            USS_Arleigh_Burke_IIa,
            "USS Ramage",
            Point(self.position.x + 6482, self.position.y + 6667),
            self.heading,
        )

        self.add_unit_to_group(
            aux_group,
            USS_Arleigh_Burke_IIa,
            "USS Mitscher",
            Point(self.position.x - 7963, self.position.y + 7037),
            self.heading,
        )

        self.add_unit_to_group(
            aux_group,
            USS_Arleigh_Burke_IIa,
            "USS Forrest Sherman",
            Point(self.position.x - 7408, self.position.y - 7408),
            self.heading,
        )

        self.add_unit_to_group(
            aux_group,
            USS_Arleigh_Burke_IIa,
            "USS Lassen",
            Point(self.position.x + 8704, self.position.y - 6296),
            self.heading,
        )

        # Add Ticonderoga escort
        if self.heading >= Heading.from_degrees(180):
            self.add_unit_to_group(
                aux_group,
                TICONDEROG,
                "USS Hué City",
                Point(self.position.x + 2222, self.position.y - 3333),
                self.heading,
            )
        else:
            self.add_unit_to_group(
                aux_group,
                TICONDEROG,
                "USS Hué City",
                Point(self.position.x - 3333, self.position.y + 2222),
                self.heading,
            )

        self.get_generated_group().points[0].speed = 20
