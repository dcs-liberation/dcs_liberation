import random

from game import Game
from game.dcs.groundunittype import GroundUnitType
from game.theater.theatergroundobject import VehicleGroupGroundObject
from gen.sam.group_generator import GroupGenerator


class ArmoredGroupGenerator(GroupGenerator):
    def __init__(
        self,
        game: Game,
        ground_object: VehicleGroupGroundObject,
        unit_type: GroundUnitType,
    ) -> None:
        super().__init__(game, ground_object)
        self.unit_type = unit_type

    def generate(self) -> None:
        index = 0
        for i in range(4):
            index = index + 1
            spacing_x = random.randint(30, 80)
            spacing_y = random.randint(30, 80)
            self.add_unit(
                self.unit_type.dcs_unit_type,
                "Armor#" + str(index),
                self.position.x + spacing_x * i,
                self.position.y + spacing_y * i,
                self.heading,
            )


class FixedSizeArmorGroupGenerator(GroupGenerator):
    def __init__(
        self,
        game: Game,
        ground_object: VehicleGroupGroundObject,
        unit_type: GroundUnitType,
        size: int,
    ) -> None:
        super().__init__(game, ground_object)
        self.unit_type = unit_type
        self.size = size

    def generate(self):
        spacing = random.randint(20, 70)

        index = 0
        for i in range(self.size):
            index = index + 1
            self.add_unit(
                self.unit_type.dcs_unit_type,
                "Armor#" + str(index),
                self.position.x + spacing * i,
                self.position.y,
                self.heading,
            )
