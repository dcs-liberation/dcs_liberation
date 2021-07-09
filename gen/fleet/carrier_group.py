import random

from gen.sam.group_generator import ShipGroupGenerator

from dcs.ships import USS_Arleigh_Burke_IIa, TICONDEROG


class CarrierGroupGenerator(ShipGroupGenerator):
    def generate(self) -> None:

        # Carrier Strike Group 8
        if self.faction.carrier_names[0] == "Carrier Strike Group 8":
            carrier_type = random.choice(self.faction.aircraft_carrier)

            self.add_unit(
                carrier_type,
                "CVN-75 Harry S. Truman",
                self.position.x,
                self.position.y,
                self.heading,
            )

            # Add Arleigh Burke escort
            self.add_unit(
                USS_Arleigh_Burke_IIa,
                "USS Ramage",
                self.position.x + 6482,
                self.position.y + 6667,
                self.heading,
            )

            self.add_unit(
                USS_Arleigh_Burke_IIa,
                "USS Mitscher",
                self.position.x - 7963,
                self.position.y + 7037,
                self.heading,
            )

            self.add_unit(
                USS_Arleigh_Burke_IIa,
                "USS Forrest Sherman",
                self.position.x - 7408,
                self.position.y - 7408,
                self.heading,
            )

            self.add_unit(
                USS_Arleigh_Burke_IIa,
                "USS Lassen",
                self.position.x + 8704,
                self.position.y - 6296,
                self.heading,
            )

            # Add Ticonderoga escort
            if self.heading >= 180:
                self.add_unit(
                    TICONDEROG,
                    "USS Hué City",
                    self.position.x + 2222,
                    self.position.y - 3333,
                    self.heading,
                )
            else:
                self.add_unit(
                    TICONDEROG,
                    "USS Hué City",
                    self.position.x - 3333,
                    self.position.y + 2222,
                    self.heading,
                )

            self.get_generated_group().points[0].speed = 20
        ##################################################################################################
        # Add carrier for normal generation
        else:
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

            # Add destroyers escort
            if len(self.faction.destroyers) > 0:
                dd_type = random.choice(self.faction.destroyers)
                self.add_unit(
                    dd_type,
                    "DD1",
                    self.position.x + 2500,
                    self.position.y + 4500,
                    self.heading,
                )
                self.add_unit(
                    dd_type,
                    "DD2",
                    self.position.x + 2500,
                    self.position.y - 4500,
                    self.heading,
                )

                self.add_unit(
                    dd_type,
                    "DD3",
                    self.position.x + 4500,
                    self.position.y + 8500,
                    self.heading,
                )
                self.add_unit(
                    dd_type,
                    "DD4",
                    self.position.x + 4500,
                    self.position.y - 8500,
                    self.heading,
                )

            self.get_generated_group().points[0].speed = 20
